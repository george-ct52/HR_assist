import gradio as gr

from graph import run_query
from db_creator import SAMPLE_ROWS


EMPLOYEE_CHOICES = [
    (f"{row[1]} ({row[0]})", row[0])
    for row in SAMPLE_ROWS
]


def chat_fn(message, history, employee_id):
    try:
        result = run_query(
            message,
            employee_id=employee_id
        )
    except Exception as e:
        return f"Something went wrong: {e}"

    route = result.get("route", "?")
    answer = result.get(
        "answer",
        "No answer generated."
    )

    return f"{answer}\n\n*[routed as: {route}]*"


with gr.Blocks(title="HR Assistant") as demo:

    gr.Markdown(
        "# HR Assistant\n"
        "Ask about your employee data, HR policies, or both."
    )

    employee_dropdown = gr.Dropdown(
        choices=EMPLOYEE_CHOICES,
        value=EMPLOYEE_CHOICES[0][1],
        label="Logged in as",
    )

    gr.ChatInterface(
        fn=chat_fn,
        additional_inputs=[employee_dropdown],
        examples=[
            ["What is my leave balance?", "E1001"],
            ["What is the company's maternity leave policy?", "E1001"],
            ["Can I carry forward my remaining leave days?", "E1001"],
            ["Who is my manager?", "E1001"],
            ["What is the WFH policy?", "E1001"],
        ],
    )


if __name__ == "__main__":
    demo.launch()