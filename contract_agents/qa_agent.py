import json

from contract_schemas.qa_schema import QASchema
from contract_tools.llm_client import client


def run_qa_fallback(scope_data: dict, plan_data: dict, assets: list) -> QASchema:
    missing_items = []
    risk_flags = []
    revision_suggestions = []

    if not scope_data.get("goal"):
        missing_items.append("Goal is missing from scope data.")

    if not plan_data.get("tasks"):
        missing_items.append("Execution tasks are missing.")

    if not assets:
        missing_items.append("No generated assets were found.")

    if scope_data.get("missing_info"):
        risk_flags.append("There is unresolved missing information from intake.")

    revision_suggestions.append("Review all generated outputs manually before client delivery.")

    coverage_score = max(0, 100 - (len(missing_items) * 20) - (len(risk_flags) * 10))
    ready_for_review = len(missing_items) == 0

    return QASchema(
        coverage_score=coverage_score,
        missing_items=missing_items,
        risk_flags=risk_flags,
        revision_suggestions=revision_suggestions,
        ready_for_review=ready_for_review
    )


def run_qa(scope_data: dict, plan_data: dict, assets: list, use_ai: bool = True) -> QASchema:
    if not use_ai:
        return run_qa_fallback(scope_data, plan_data, assets)

    system_prompt = """
You are the QA Agent for an AI Contract Execution Engine.

Your job is to review the scope, plan, and generated assets before a human delivers them.

Check for:
- missing requirements
- weak assumptions
- unsupported claims
- vague deliverables
- missing client-provided documents
- risks in implementation
- whether the package is ready for human review

Be honest. Do not overrate incomplete work.
A project can be ready for human review even if it is not ready for client delivery.
"""

    user_prompt = f"""
Scope data:
{json.dumps(scope_data, indent=2)}

Plan data:
{json.dumps(plan_data, indent=2)}

Generated assets:
{json.dumps(assets, indent=2)}

Return a QA review.
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
                    "name": "qa_schema",
                    "schema": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "coverage_score": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 100
                            },
                            "missing_items": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "risk_flags": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "revision_suggestions": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "ready_for_review": {
                                "type": "boolean"
                            }
                        },
                        "required": [
                            "coverage_score",
                            "missing_items",
                            "risk_flags",
                            "revision_suggestions",
                            "ready_for_review"
                        ]
                    },
                    "strict": True
                }
            }
        )

        qa_dict = json.loads(response.output_text)
        return QASchema(**qa_dict)

    except Exception as e:
        print(f"OpenAI QA failed. Falling back to default QA. Error: {e}")
        return run_qa_fallback(scope_data, plan_data, assets)