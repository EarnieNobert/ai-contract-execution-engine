import json
from openai import OpenAI

from contract_schemas.intake_schema import IntakeSchema
from contract_tools.llm_client import client


VALID_PROJECT_TYPES = ["chatbot", "data_analysis", "ai_tutor"]


def detect_project_type(raw_request: str) -> str:
    """
    Fallback keyword-based project detection.
    Used only if the OpenAI-powered intake call fails.
    """
    text = raw_request.lower()

    tutor_keywords = [
        "tutor", "lesson", "lessons", "quiz", "quizzes", "learning",
        "teach", "teaches", "student", "students", "grade", "grades",
        "grading", "curriculum", "practice", "coach"
    ]

    data_keywords = [
        "csv", "spreadsheet", "spreadsheets", "excel", "analysis",
        "analyze", "review this spreadsheet", "dashboard", "data",
        "kpi", "metrics", "report", "insights", "trends", "trend",
        "sales", "revenue", "monthly", "chart", "charts"
    ]

    chatbot_keywords = [
        "chatbot", "faq", "support bot", "customer support",
        "knowledge base", "policy assistant", "service policies",
        "answer customer questions"
    ]

    if any(keyword in text for keyword in tutor_keywords):
        return "ai_tutor"

    if any(keyword in text for keyword in data_keywords):
        return "data_analysis"

    if any(keyword in text for keyword in chatbot_keywords):
        return "chatbot"

    return "chatbot"


def generate_intake_fallback(
    contract_name: str,
    client_name: str,
    raw_request: str,
    constraints: str,
    deadline: str,
    notes: str
) -> IntakeSchema:
    """
    Safe fallback when the OpenAI API is unavailable.
    """
    project_type = detect_project_type(raw_request)

    return IntakeSchema(
        contract_name=contract_name,
        client_name=client_name,
        project_type=project_type,
        goal=raw_request.strip(),
        deliverables=[
            "Draft scope",
            "Execution plan",
            "Starter assets",
            "QA report"
        ],
        constraints=[
            c.strip()
            for c in constraints.split("\n")
            if c.strip()
        ],
        deadline=deadline,
        notes=notes,
        assumptions=[
            "This is an initial draft based on the provided request."
        ],
        missing_info=[
            "Specific technical requirements may still be needed."
        ],
        source_docs_needed=[
            "Any existing documentation, examples, or files from the client."
        ],
        risks=[
            "Incomplete client requirements may affect output quality."
        ]
    )


def generate_intake(
    contract_name: str,
    client_name: str,
    raw_request: str,
    constraints: str,
    deadline: str,
    notes: str,
    use_ai: bool = True
) -> IntakeSchema:
    """
    OpenAI-powered Intake Agent.

    Converts messy client request text into structured project scope data.
    Falls back to keyword logic if the API call fails.
    """

    if not use_ai:
        return generate_intake_fallback(
            contract_name=contract_name,
            client_name=client_name,
            raw_request=raw_request,
            constraints=constraints,
            deadline=deadline,
            notes=notes
        )

    system_prompt = """
You are the Intake Agent for an AI Contract Execution Engine.

Your job is to convert a signed client request into structured project intake data.

You must classify the project_type as exactly one of:
- chatbot
- data_analysis
- ai_tutor

Definitions:
- chatbot: FAQ bot, customer support assistant, internal knowledge assistant, policy assistant
- data_analysis: CSV/spreadsheet analysis, dashboards, KPIs, metrics, reports, trends, business insights
- ai_tutor: learning assistant, lessons, quizzes, grading, curriculum, practice coach

Be practical and honest. Do not pretend the client provided information that is missing.
If details are missing, add them to missing_info.
If assumptions are needed, list them clearly.
"""

    user_prompt = f"""
Contract Name: {contract_name}
Client Name: {client_name}
Raw Client Request:
{raw_request}

Constraints:
{constraints}

Deadline:
{deadline}

Notes:
{notes}

Return structured intake data for this contract.
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
                    "name": "intake_schema",
                    "schema": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "contract_name": {"type": "string"},
                            "client_name": {"type": "string"},
                            "project_type": {
                                "type": "string",
                                "enum": VALID_PROJECT_TYPES
                            },
                            "goal": {"type": "string"},
                            "deliverables": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "constraints": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "deadline": {"type": "string"},
                            "notes": {"type": "string"},
                            "assumptions": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "missing_info": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "source_docs_needed": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "risks": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        },
                        "required": [
                            "contract_name",
                            "client_name",
                            "project_type",
                            "goal",
                            "deliverables",
                            "constraints",
                            "deadline",
                            "notes",
                            "assumptions",
                            "missing_info",
                            "source_docs_needed",
                            "risks"
                        ]
                    },
                    "strict": True
                }
            }
        )

        intake_dict = json.loads(response.output_text)
        return IntakeSchema(**intake_dict)

    except Exception as e:
        print(f"OpenAI intake failed. Falling back to keyword logic. Error: {e}")

        return generate_intake_fallback(
            contract_name=contract_name,
            client_name=client_name,
            raw_request=raw_request,
            constraints=constraints,
            deadline=deadline,
            notes=notes
        )