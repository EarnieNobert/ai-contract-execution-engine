from contract_schemas.intake_schema import IntakeSchema


def detect_project_type(raw_request: str) -> str:
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


def generate_intake(
    contract_name: str,
    client_name: str,
    raw_request: str,
    constraints: str,
    deadline: str,
    notes: str
) -> IntakeSchema:
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