def generate_chatbot_assets(scope_data: dict, plan_data: dict):
    return [
        {
            "artifact_type": "markdown",
            "filename": "chatbot_scope.md",
            "content": f"# Chatbot Scope\n\nGoal: {scope_data.get('goal', '')}\n"
        },
        {
            "artifact_type": "json",
            "filename": "test_cases.json",
            "content": """[
  {"input": "What are your business hours?", "expected_behavior": "Answer from company policy if available."},
  {"input": "Can I get a refund?", "expected_behavior": "Use refund policy or escalate if policy is missing."}
]"""
        },
        {
            "artifact_type": "python",
            "filename": "starter_chatbot_app.py",
            "content": """import streamlit as st

st.title("Starter Chatbot App")
user_input = st.text_input("Ask a question")
if user_input:
    st.write("This is where chatbot logic will go.")
"""
        }
    ]