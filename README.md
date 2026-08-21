# HR Assist

An AI-powered **HR Assistant** that answers employee questions using a combination of **structured employee data** and **company HR policies**.

The system uses **LangGraph** to orchestrate the workflow and intelligently routes each question to the appropriate data source:

```text
                         User
                           │
                           ▼
                      HR Assistant
                           │
                           ▼
                      Query Router
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
             SQL         VECTOR        BOTH
              │            │            │
              ▼            ▼            ▼
        Employee DB    Policy DB    SQL + Vector
              │            │            │
              └────────────┼────────────┘
                           ▼
                    Answer Synthesis
                           │
                           ▼
                         Answer
```

## Features

* 🤖 Natural-language HR question answering
* 🔀 Intelligent query routing using LangGraph
* 🗄️ Structured employee information retrieval using SQLite
* 📚 Policy document retrieval using ChromaDB
* 🔎 Semantic search using Hugging Face embeddings
* 🧠 LLM-powered SQL generation
* 📝 LLM-powered answer synthesis
* 👤 Employee selection through a Gradio interface
* 🔐 Read-only SQL queries
* 🏠 Local LLM support through Ollama
* ⚡ Groq support for fast cloud inference

## Example Questions

### Employee data

```text
What is my leave balance?
Who is my manager?
What department do I work in?
What is my salary?
When did I join the company?
```

These questions are routed to:

```text
SQL → Employee Database
```

### HR policy questions

```text
What is the company's maternity leave policy?
What is the WFH policy?
How many days of annual leave do employees get?
```

These are routed to:

```text
VECTOR → Policy Vector Database
```

### Questions requiring both

```text
Can I carry forward my remaining leave days?
```

This requires:

```text
Employee DB → Current leave balance
       +
Policy DB → Leave carry-forward rules
```

Therefore:

```text
BOTH → SQL + Vector Search
```

---

# Architecture

## 1. Query Router

The router determines which source is required to answer the question:

```text
SQL
VECTOR
BOTH
```

For example:

```text
"What is my leave balance?"
        ↓
       SQL
```

while:

```text
"Can I carry forward my remaining leave?"
        ↓
       BOTH
```

The router is implemented as a LangGraph node.

---

## 2. SQL Tool

The SQL tool handles structured, employee-specific information.

The employee database contains fields such as:

```text
employee_id
name
department
manager_name
salary
joining_date
leave_balance
```

The LLM converts the employee's natural-language question into a SQL `SELECT` query.

Example:

```text
"What is my leave balance?"
             ↓
SELECT leave_balance
FROM employees
WHERE employee_id = 'E1001'
```

Only read-only `SELECT` queries are permitted.

---

## 3. Vector Search

Company policy documents are stored as `.txt` files:

```text
data/
└── policies/
    ├── leave_policy.txt
    ├── wfh_policy.txt
    ├── maternity_policy.txt
    └── insurance_policy.txt
```

The documents are:

```text
Documents
    ↓
Text splitting
    ↓
Chunks
    ↓
Embeddings
    ↓
ChromaDB
```

The application then performs semantic similarity search to retrieve relevant policy chunks.

The embedding model currently used is:

```text
sentence-transformers/all-MiniLM-L6-v2
```

---

## 4. LangGraph

LangGraph orchestrates the complete workflow:

```text
START
  │
  ▼
Router
  │
  ├── SQL ────────┐
  │               │
  ├── VECTOR ─────┤
  │               ▼
  └── BOTH ───► Answer
                  │
                  ▼
                 END
```

The routing happens **once before retrieval**, keeping the workflow simple and predictable.

---

# Tech Stack

| Component           | Technology                         |
| ------------------- | ---------------------------------- |
| Frontend            | Gradio                             |
| Orchestration       | LangGraph                          |
| LLM                 | Ollama / Groq                      |
| SQL Database        | SQLite                             |
| Vector Database     | ChromaDB                           |
| Embeddings          | Hugging Face Sentence Transformers |
| Backend             | Python                             |
| Document Processing | LangChain                          |
| Model               | Llama / GPT-OSS models             |

---

# Project Structure

HR_assist/
│
├── app.py                    # Gradio frontend
├── graph.py                  # LangGraph workflow
├── router.py                 # Query routing
├── vector_store.py           # Builds Chroma vector database
├── db_creator.py             # Creates sample employee database
│
├── tools/
│   ├── __init__.py
│   ├── sql_tool.py           # Employee database queries
│   └── vector_tool.py        # Policy document retrieval
│
├── data/
│   ├── employees.db          # SQLite employee database
│   │
│   ├── policies/             # HR policy documents
│   │   ├── leave_policy.txt
│   │   ├── wfh_policy.txt
│   │   └── maternity_policy.txt
│   │
│   └── chroma_db/            # Persistent Chroma database
│
├── requirements.txt
└── README.md


---

# Installation

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd HR_assist
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```



## Using Groq

If using Groq, configure your API key:

```bash
export GROQ_API_KEY="your_api_key"
```

You can then use a supported Groq model through `ChatGroq`.

---

# Create the Employee Database

Run:

```bash
python db_creator.py
```

This creates the SQLite employee database used by the SQL tool.

---

# Build the Policy Vector Database

After adding your policy `.txt` files to:

```text
data/policies/
```

run:

```bash
python vector_store.py
```

This will:

1. Load policy documents
2. Split documents into chunks
3. Generate embeddings
4. Store the embeddings in ChromaDB

The resulting database is stored in:

```text
data/chroma_db/
```

---

# Run the Application

Start the Gradio application:

```bash
python app.py
```

Gradio will provide a local URL where you can interact with HR Assist.

Select an employee from the **Logged in as** dropdown and ask a question.

Example:

```text
Can I carry forward my remaining leave days?
```

The system will:

```text
Question
   ↓
Router
   ↓
BOTH
   ↓
Employee DB + Policy DB
   ↓
LLM
   ↓
Final Answer
```

---

# Example

Suppose employee `E1001` has:

```text
Leave balance: 8 days
```

and the company policy says:

```text
Employees may carry forward a maximum of 5 unused leave days.
```

The user asks:

```text
Can I carry forward my remaining leave days?
```

The router selects:

```text
BOTH
```

SQL retrieves:

```text
leave_balance = 8
```

Vector search retrieves:

```text
Maximum carry-forward = 5 days
```

The final LLM produces an answer such as:

```text
You currently have 8 leave days remaining. According to the
company policy, you can carry forward up to 5 days.
```

---

# Security Considerations

The SQL tool is designed for read-only access.

Generated SQL is validated before execution to prevent operations such as:

```text
INSERT
UPDATE
DELETE
DROP
ALTER
ATTACH
PRAGMA
```

Only `SELECT` queries are permitted.

For a production deployment, additional controls should be implemented, including:

* Parameterized SQL queries
* Database-level read-only permissions
* Authentication and authorization
* Employee-level access control
* Audit logging
* Prompt-injection protection
* Secrets management
* Input validation

---

# Future Improvements

* [ ] Add authentication and employee login
* [ ] Add conversation memory
* [ ] Improve query routing with structured output
* [ ] Add more HR data sources
* [ ] Add document upload functionality
* [ ] Add citations to retrieved policy documents
* [ ] Add evaluation using RAG evaluation metrics
* [ ] Add automated tests for SQL generation and retrieval
* [ ] Add observability and LangGraph tracing
* [ ] Deploy the application to the cloud
* [ ] Add role-based access for HR administrators

---

# Learning Goals

This project demonstrates practical use of:

* **LangGraph orchestration**
* **RAG**
* **Vector databases**
* **Embeddings**
* **Natural-language-to-SQL**
* **LLM routing**
* **Tool-based retrieval**
* **Prompt engineering**
* **Gradio**
* **Local and hosted LLM inference**

The main design principle is to **use structured retrieval for structured questions and semantic retrieval for unstructured policy information**, while combining both when a question requires employee-specific data and policy context.
