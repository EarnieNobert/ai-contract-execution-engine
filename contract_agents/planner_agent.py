import json

from contract_schemas.plan_schema import PlanSchema
from contract_tools.llm_client import client


def generate_plan_fallback(scope_data: dict) -> PlanSchema:
    project_type = scope_data.get("project_type", "")

    recommended_stack = ["Python", "Streamlit", "OpenAI API", "Pydantic"]

    if project_type == "chatbot":
        recommended_stack.append("Prompt-based chatbot workflow")
    elif project_type == "data_analysis":
        recommended_stack.append("Pandas")
    elif project_type == "ai_tutor":
        recommended_stack.append("Lesson and quiz workflow")

    return PlanSchema(
        milestones=[
            "Finalize scope",
            "Generate starter assets",
            "Run QA review",
            "Prepare export package"
        ],
        tasks=[
            "Review intake details",
            "Confirm project type and deliverables",
            "Create initial implementation assets",
            "Review risks and missing information",
            "Prepare draft handoff package"
        ],
        dependencies=[
            "Scope must be generated before planning",
            "Plan must be generated before assets",
            "Assets must exist before QA"
        ],
        recommended_stack=recommended_stack,
        validation_checks=[
            "Does the plan match the client's goal?",
            "Are all major deliverables included?",
            "Are assumptions clearly stated?"
        ],
        risk_register=[
            "Client request may be incomplete",
            "Generated artifacts are first-pass drafts only",
            "Human review is required before delivery"
        ]
    )


def generate_plan(scope_data: dict, use_ai: bool = True) -> PlanSchema:
    if not use_ai:
        return generate_plan_fallback(scope_data)

    system_prompt = """
You are the Planner Agent for an AI Contract Execution Engine.

Your job is to turn structured project scope into a realistic execution plan.

Create a plan that is specific to the project_type:
- chatbot
- data_analysis
- ai_tutor

Be practical. Include human review checkpoints.
Do not pretend missing information has been provided.
"""

    user_prompt = f"""
Structured scope data:
{json.dumps(scope_data, indent=2)}

Return a practical execution plan.
"""

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "plan_schema",
                    "schema": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "milestones": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "tasks": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "dependencies": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "recommended_stack": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "validation_checks": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "risk_register": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        },
                        "required": [
                            "milestones",
                            "tasks",
                            "dependencies",
                            "recommended_stack",
                            "validation_checks",
                            "risk_register"
                        ]
                    },
                    "strict": True
                }
            }
        )

        plan_dict = json.loads(response.output_text)
        return PlanSchema(**plan_dict)

    except Exception as e:
        print(f"OpenAI planner failed. Falling back to default plan. Error: {e}")
        return generate_plan_fallback(scope_data)