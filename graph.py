from typing import Optional, TypedDict

from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama

from router import route_query
from sql_tool import query_employee_data
from vector_tool import query_policy_docs

CHAT_MODEL = "llama3.1"


class HRState(TypedDict, total=False):
    query: str
    employee_id: str
    route: str
    sql_result: Optional[str]
    vector_result: Optional[str]
    answer: str

llm=ChatOllama(model=CHAT_MODEL, temperature=0.2)

def router_node(state: HRState) -> Hr:
    route = route_query(state["query"], llm=llm)
    state["route"] = route

