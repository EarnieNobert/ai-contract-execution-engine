import streamlit as st

from contract_agents.intake_agent import generate_intake
from contract_agents.planner_agent import generate_plan
from contract_agents.builder_agent import generate_assets
from contract_agents.qa_agent import run_qa
from contract_tools.export_tools import export_contract_package


st.set_page_config(page_title="AI Contract Execution Engine", layout="wide")

st.title("AI Contract Execution Engine")
st.caption("Turn a signed client request into scoped plans, starter assets, QA, and exportable delivery packages.")

if "scope_data" not in st.session_state:
    st.session_state.scope_data = None

if "plan_data" not in st.session_state:
    st.session_state.plan_data = None

if "assets" not in st.session_state:
    st.session_state.assets = []

if "qa_data" not in st.session_state:
    st.session_state.qa_data = None


tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Contract Intake",
    "Scope Builder",
    "Execution Plan",
    "Asset Generator",
    "QA Review",
    "Export Package"
])

with tab1:
    st.subheader("Contract Intake")

    contract_name = st.text_input("Contract Name")
    client_name = st.text_input("Client Name")
    raw_request = st.text_area("Raw Client Request", height=200)
    constraints = st.text_area("Constraints (one per line)", height=120)
    deadline = st.text_input("Deadline")
    notes = st.text_area("Notes", height=120)

    if st.button("Analyze Request"):
        scope = generate_intake(
            contract_name=contract_name,
            client_name=client_name,
            raw_request=raw_request,
            constraints=constraints,
            deadline=deadline,
            notes=notes
        )
        st.session_state.scope_data = scope.model_dump()
        st.success("Intake analysis complete.")
        st.json(st.session_state.scope_data)

with tab2:
    st.subheader("Scope Builder")

    if st.session_state.scope_data:
        st.json(st.session_state.scope_data)
    else:
        st.info("Analyze a contract request first in the Contract Intake tab.")

with tab3:
    st.subheader("Execution Plan")

    if st.button("Generate Plan"):
        if st.session_state.scope_data:
            plan = generate_plan(st.session_state.scope_data)
            st.session_state.plan_data = plan.model_dump()
            st.success("Execution plan generated.")
        else:
            st.warning("You need scope data before generating a plan.")

    if st.session_state.plan_data:
        st.json(st.session_state.plan_data)

with tab4:
    st.subheader("Asset Generator")

    if st.button("Generate Assets"):
        if st.session_state.scope_data and st.session_state.plan_data:
            assets = generate_assets(
                st.session_state.scope_data,
                st.session_state.plan_data
            )
            st.session_state.assets = assets
            st.success("Assets generated.")
        else:
            st.warning("You need scope and plan data before generating assets.")

    if st.session_state.assets:
        for asset in st.session_state.assets:
            st.markdown(f"### {asset.get('filename', 'Untitled')}")
            st.code(asset.get("content", ""), language="python" if asset.get("filename", "").endswith(".py") else "text")

with tab5:
    st.subheader("QA Review")

    if st.button("Run QA"):
        if st.session_state.scope_data and st.session_state.plan_data and st.session_state.assets:
            qa = run_qa(
                st.session_state.scope_data,
                st.session_state.plan_data,
                st.session_state.assets
            )
            st.session_state.qa_data = qa.model_dump()
            st.success("QA completed.")
        else:
            st.warning("You need scope, plan, and assets before running QA.")

    if st.session_state.qa_data:
        st.json(st.session_state.qa_data)

with tab6:
    st.subheader("Export Package")

    if st.button("Export Package"):
        if st.session_state.scope_data and st.session_state.plan_data and st.session_state.qa_data:
            export_path = export_contract_package(
                contract_name=st.session_state.scope_data.get("contract_name", "untitled_contract"),
                scope_data=st.session_state.scope_data,
                plan_data=st.session_state.plan_data,
                qa_data=st.session_state.qa_data,
                assets=st.session_state.assets
            )
            st.success(f"Package exported to: {export_path}")
        else:
            st.warning("You need scope, plan, assets, and QA before export.")