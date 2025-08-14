import streamlit as st
from azure.ai.projects import AIProjectClient
#from azure.identity import AzureCliCredential
from azure.ai.agents.models import ListSortOrder
import time

from azure.identity import ClientSecretCredential
import streamlit as st

# credential = ClientSecretCredential(
#     tenant_id=st.secrets["4f095feb-16b0-45ff-b055-bd46904c486c"],
#     client_id=st.secrets["f54b9c82-c844-4d75-a5ae-c7dc996b319e"],
#     client_secret=st.secrets["utB8Q~tTexojFQM03_fRG0JhxfR1n2IUtB1i~c04"]
# )


# ---------------------
# Azure Project Setup
# ---------------------
@st.cache_resource
def load_agent():
    credential = ClientSecretCredential(
        tenant_id=st.secrets["AZURE_TENANT_ID"],
        client_id=st.secrets["AZURE_CLIENT_ID"],
        client_secret=st.secrets["AZURE_CLIENT_SECRET"]
    )

    client = AIProjectClient(
        credential=credential,
        endpoint="https://aqnaz-me7h81i9-eastus2.services.ai.azure.com/api/projects/aqnaz-me7h81i9-eastus2_project"
    )
    return client, client.agents.get_agent("asst_FKK010NLy2Wq7lDf5leaZi8n")


project, agent = load_agent()

# ---------------------
# Streamlit Page Setup
# ---------------------
st.set_page_config(page_title="Liberty Work Order Assistant", layout="wide")
st.markdown(
    """
    <style>
        .main { background-color: #f0f4f8; }
        .header { background-color: #003366; color: white; padding: 10px 20px; display: flex; align-items: center; gap: 15px; }
        .header img { height: 40px; }
        .header h1 { font-size: 22px; margin: 0; }
        .wo-card { background-color: #e6f2ff; border: 1px solid #b3d1ff; border-radius: 6px; padding: 12px; margin-bottom: 15px; box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.05); }
        .wo-card h3 { margin: 0 0 8px; color: #004080; }
        .chatbox {
            border: 1px solid #ccc;
            border-radius: 6px;
            padding: 10px 15px;
            background: #ffffff;
            max-height: 50vh;           /* Limit height for better layout */
            min-height: 120px;          /* Prevent collapsing */
            overflow-y: auto;
            margin-bottom: 0;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }
        .user-msg, .bot-msg {
            margin-bottom: 8px;         /* Less vertical spacing between messages */
            line-height: 1.4;
            font-size: 14px;
        }
        .user-msg strong, .bot-msg strong {
            font-weight: 600;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------
# Header
# ---------------------
st.markdown(
    '<div class="header"><img src="https://www.stlawrencegas.com/wp-content/uploads/2020/11/Liberty_Logo_Horizontal_rev.png"><h1>Liberty Work Order Assistant</h1></div>',
    unsafe_allow_html=True
)

# ---------------------
# Layout Columns
# ---------------------
col1, col2 = st.columns([1, 2])

# Sidebar: Work Orders
with col1:
    st.subheader("📋 Work Orders")

    work_orders = {
        "WO123456": {"status": "In Progress", "meter": "MTR98765", "crew": "Team A"},
        "WO789012": {"status": "Completed", "meter": "MTR65432", "crew": "Team B"},
        "WO345678": {"status": "Pending", "meter": "MTR32109", "crew": "Team C"},
    }

    selected_wo = st.radio("Select a work order:", list(work_orders.keys()))

    for wo, details in work_orders.items():
        with st.container():
            st.markdown(f"""
            <div class="wo-card">
                <h3>{wo}</h3>
                <p><strong>Status:</strong> {details["status"]}</p>
                <p><strong>Meter ID:</strong> {details["meter"]}</p>
                <p><strong>Crew:</strong> {details["crew"]}</p>
            </div>
            """, unsafe_allow_html=True)

# Chat & Assistant
with col2:
    st.subheader("💬 Chat with Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.thread_id = project.agents.threads.create().id

    # Input area
    with st.form("chat_form", clear_on_submit=True):
        default_prompt = f"Give me a status update on {selected_wo}"
        user_input = st.text_input("Your Message:", value=default_prompt)
        submitted = st.form_submit_button("Send")

    # Send message to agent
    if submitted and user_input:
        st.session_state.messages.append(("user", user_input))

        # Send user input to Azure agent
        project.agents.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=user_input
        )

        run = project.agents.runs.create_and_process(
            thread_id=st.session_state.thread_id,
            agent_id=agent.id
        )

        with st.spinner("Agent is thinking..."):
            timeout = 30
            start = time.time()
            while run.status in ["queued", "in_progress"]:
                if time.time() - start > timeout:
                    break
                time.sleep(1)
                run = project.agents.runs.get(thread_id=st.session_state.thread_id, run_id=run.id)

        # Fetch response
        if run.status == "failed":
            st.session_state.messages.append(("agent", f"❌ Error: {run.last_error.get('message')}"))
        else:
            messages = project.agents.messages.list(thread_id=st.session_state.thread_id, order=ListSortOrder.ASCENDING)
            for msg in messages:
                if msg.role == "assistant" and msg.text_messages:
                    last = msg.text_messages[-1].text.value
                    st.session_state.messages.append(("agent", last))

    # Display chat
    with st.container():
        st.markdown('<div class="chatbox">', unsafe_allow_html=True)
        for role, msg in st.session_state.messages:
            if role == "user":
                st.markdown(f'<div class="user-msg"><strong>You:</strong> {msg}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-msg"><strong>Agent:</strong><br>{msg}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
