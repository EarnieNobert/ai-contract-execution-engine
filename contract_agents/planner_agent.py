from contract_schemas.plan_schema import PlanSchema


def generate_plan(scope_data: dict) -> PlanSchema:
    project_type = scope_data.get("project_type", "")

    milestones = [
        "Finalize scope",
        "Generate starter assets",
        "Run QA review",
        "Prepare export package"
    ]

    tasks = [
        "Review intake details",
        "Confirm project type and deliverables",
        "Create initial implementation assets",
        "Review risks and missing information",
        "Prepare draft handoff package"
    ]

    dependencies = [
        "Scope must be generated before planning",
        "Plan must be generated before assets",
        "Assets must exist before QA"
    ]

    recommended_stack = ["Python", "Streamlit", "OpenAI API", "Pydantic"]

    if project_type == "chatbot":
        recommended_stack.append("Prompt-based chatbot workflow")
    elif project_type == "data_analysis":
        recommended_stack.append("Pandas")
    elif project_type == "ai_tutor":
        recommended_stack.append("Lesson and quiz workflow")

    validation_checks = [
        "Does the plan match the client's goal?",
        "Are all major deliverables included?",
        "Are assumptions clearly stated?"
    ]

    risk_register = [
        "Client request may be incomplete",
        "Generated artifacts are first-pass drafts only",
        "Human review is required before delivery"
    ]

    return PlanSchema(
        milestones=milestones,
        tasks=tasks,
        dependencies=dependencies,
        recommended_stack=recommended_stack,
        validation_checks=validation_checks,
        risk_register=risk_register
    )