from contract_agents.intake_agent import generate_intake


def test_generate_intake():
    result = generate_intake(
        contract_name="Test Contract",
        client_name="Test Client",
        raw_request="Build a chatbot for a small company",
        constraints="Use Streamlit",
        deadline="Next month",
        notes="Test notes"
    )

    assert result.project_type == "chatbot"
    assert result.contract_name == "Test Contract"