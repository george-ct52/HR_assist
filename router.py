

SQL_KEYWORDS = [
    "salary", "leave balance", "leave days", "joining date", "date of joining",
    "employee id", "manager", "department", "attendance", "how many leave",
]
POLICY_KEYWORDS = [
    "policy", "policies", "rules", "eligibility", "eligible", "procedure",
    "allowed", "carry forward", "carried forward", "work from home", "wfh",
    "insurance", "maternity", "paternity", "sick leave rules",
]


def keyword_route(query: str) -> str:
    q = query.lower()
    needs_sql = any(k in q for k in SQL_KEYWORDS)
    needs_vector = any(k in q for k in POLICY_KEYWORDS)
    if needs_sql and needs_vector:
        return "BOTH"
    if needs_sql:
        return "SQL"
    if needs_vector:
        return "VECTOR"
    return "VECTOR" 




