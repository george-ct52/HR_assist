from typing import Optional, TypedDict

from langgraph import graph
from langgraph.graph import StateGraph, END
#from langchain_ollama import ChatOllama
from langchain_groq.chat_models import ChatGroq
from router import keyword_route
from tools.sql_tool import query_employee_data
from tools.vector_tool import query_policy_docs
from dotenv import load_dotenv
import os
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CHAT_MODEL = "openai/gpt-oss-20b"


class HRState(TypedDict, total=False):
    query: str
    employee_id: str
    route: str
    sql_result: Optional[str]
    vector_result: Optional[str]
    answer: str

#llm=ChatOllama(model=CHAT_MODEL, temperature=0.2)
llm=ChatGroq(model=CHAT_MODEL, temperature=0.2,api_key=GROQ_API_KEY)


def router_node(state: HRState) -> HRState:
    route = keyword_route(state["query"])
    state["route"] = route
    return state

def sql_node(state: HRState) -> HRState:
    result = query_employee_data(state["query"], state["employee_id"]) 
    return {"sql_result": result}


def vector_node(state: HRState) -> HRState:
    result = query_policy_docs(state["query"], k=4)
    return {"vector_result": result}


def answer_node(state: HRState) -> HRState:
    context_parts = []

    # to get the sql result 
    if state.get("sql_result"):
        context_parts.append(f"Employee data:\n{state['sql_result']}")

    #to get the vector result
    if state.get("vector_result"):
        context_parts.append(f"Relevant policy text:\n{state['vector_result']}")
    context = "\n\n".join(context_parts) if context_parts else "No context retrieved."

    prompt = (
    "You are HR Assist, an AI-powered HR assistant for employees.\n\n"

    "If the employee asks who you are, what you are, or a similar question, "
    "say that you are HR Assist, an AI-powered HR assistant that helps with "
    "employee information and company HR policies.\n\n"

    "For other questions, answer using ONLY the context below. "
    "Be concise and specific. Cite numbers where relevant. "
    "If the context doesn't fully answer the question, say what's missing.\n\n"

    f"Context:\n{context}\n\n"
    f"Question: {state['query']}"
)

    response = llm.invoke([{"role": "user", "content": prompt}])
    return {"answer": response.content.strip()}


def choose_route(state: HRState) -> str:
    # dummy fnction to give the route decision based on the state 
    return state["route"]

def both_node(state):
    sql_result = query_employee_data(
        state["query"],
        state["employee_id"],
       
    )

    vector_result = query_policy_docs(state["query"])

    return {
        "sql_result": sql_result,
        "vector_result": vector_result
    }

def build_graph():
    graph = StateGraph(HRState)

    graph.add_node("router", router_node)
    graph.add_node("sql", sql_node)
    graph.add_node("vector", vector_node)
    graph.add_node("both", both_node)
    graph.add_node("answer", answer_node)

    graph.set_entry_point("router")

    graph.add_conditional_edges(
        "router",
        choose_route,
        {
            "SQL": "sql",
            "VECTOR": "vector",
            "BOTH": "both",
        },
    )

    graph.add_edge("sql", "answer")
    graph.add_edge("vector", "answer")
    graph.add_edge("both", "answer")
    graph.add_edge("answer", END)

    return graph.compile()


compiled_graph = None


def run_query(query: str, employee_id: str = "E1001") -> HRState:
    global compiled_graph
    if compiled_graph is None:
        compiled_graph = build_graph()
    return compiled_graph.invoke({"query": query, "employee_id": employee_id})

