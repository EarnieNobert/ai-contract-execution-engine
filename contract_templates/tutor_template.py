def generate_tutor_assets(scope_data: dict, plan_data: dict):
    return [
        {
            "artifact_type": "markdown",
            "filename": "tutor_scope.md",
            "content": f"# Tutor Scope\n\nGoal: {scope_data.get('goal', '')}\n"
        },
        {
            "artifact_type": "json",
            "filename": "lesson_map.json",
            "content": """{
  "lesson_1": "Introduction",
  "lesson_2": "Core Concept Practice",
  "lesson_3": "Assessment"
}"""
        },
        {
            "artifact_type": "python",
            "filename": "starter_tutor_app.py",
            "content": """import streamlit as st

st.title("Starter Tutor App")
st.write("This is where lesson, quiz, and grading logic will go.")
"""
        }
    ]