# import streamlit as st
# from azure.ai.projects import AIProjectClient
# from azure.identity import ClientSecretCredential
# from azure.ai.agents.models import ListSortOrder
# import time

# # ---------------------------
# # Azure AD App Credentials (Hardcoded)
# # ---------------------------
# AZURE_CLIENT_ID = "f54b9c82-c844-4d75-a5ae-c7dc996b319e"
# AZURE_TENANT_ID = "4f095feb-16b0-45ff-b055-bd46904c486c"
# AZURE_CLIENT_SECRET = "utB8Q~tTexojFQM03_fRG0JhxfR1n2IUtB1i~c04"  

# # ---------------------------
# # Authenticate with Azure
# # ---------------------------
# @st.cache_resource
# def init_project():
#     credential = ClientSecretCredential(
#         tenant_id=AZURE_TENANT_ID,
#         client_id=AZURE_CLIENT_ID,
#         client_secret=AZURE_CLIENT_SECRET
#     )
#     client = AIProjectClient(
#         credential=credential,
#         endpoint="https://aqnaz-me7h81i9-eastus2.services.ai.azure.com/api/projects/aqnaz-me7h81i9-eastus2_project"
#     )
#     return client, client.agents.get_agent("asst_FKK010NLy2Wq7lDf5leaZi8n")

# project, agent = init_project()

# # ---------------------------
# # Streamlit UI Setup
# # ---------------------------
# st.set_page_config(page_title="Liberty Work Order Assistant", layout="wide")

# # Custom CSS
# st.markdown("""
# <style>
#     .header {
#         background-color: #003366;
#         color: white;
#         padding: 10px 20px;
#         display: flex;
#         align-items: center;
#         gap: 15px;
#     }
#     .header img {
#         height: 40px;
#     }
#     .header h1 {
#         font-size: 22px;
#         margin: 0;
#     }
#     .wo-card {
#         background-color: #e6f2ff;
#         border: 1px solid #b3d1ff;
#         border-radius: 6px;
#         padding: 12px;
#         margin-bottom: 15px;
#         box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.05);
#     }
#     .wo-card h3 {
#         margin: 0 0 8px;
#         color: #004080;
#     }
#     .chatbox {
#         border: 1px solid #ccc;
#         border-radius: 6px;
#         padding: 15px;
#         background: #ffffff;
#         height: 400px;
#         overflow-y: auto;
#     }
#     .user-msg {
#         color: #003366;
#         margin-bottom: 10px;
#     }
#     .bot-msg {
#         color: #006400;
#         margin-bottom: 20px;
#     }
# </style>
# """, unsafe_allow_html=True)

# # ---------------------------
# # Header Section
# # ---------------------------
# st.markdown(
#     '''
#     <div class="header">
#         <img src="https://chambermaster.blob.core.windows.net/images/customers/1613/members/871/logos/MEMBER_PAGE_HEADER/Liberty_Logo_Horizontal_RGB.PNG" alt="Liberty Logo">
#         <h1>Liberty Work Order Assistant</h1>
#     </div>
#     ''',
#     unsafe_allow_html=True
# )

# # ---------------------------
# # Session Initialization
# # ---------------------------
# if "thread_id" not in st.session_state:
#     st.session_state.thread_id = project.agents.threads.create().id
#     st.session_state.chat_history = []

# # ---------------------------
# # Layout: Sidebar and Chat
# # ---------------------------
# col1, col2 = st.columns([1, 2])

# # 📋 Sidebar - Work Orders
# with col1:
#     st.subheader("📋 Work Orders")

#     work_orders = {
#         "WO123456": {"status": "In Progress", "meter": "MTR98765", "crew": "Team A"},
#         "WO789012": {"status": "Completed", "meter": "MTR65432", "crew": "Team B"},
#         "WO345678": {"status": "Pending", "meter": "MTR32109", "crew": "Team C"},
#     }

#     selected_wo = st.radio("Select a work order:", list(work_orders.keys()))

#     for wo, details in work_orders.items():
#         st.markdown(f"""
#         <div class="wo-card">
#             <h3>{wo}</h3>
#             <p><strong>Status:</strong> {details["status"]}</p>
#             <p><strong>Meter ID:</strong> {details["meter"]}</p>
#             <p><strong>Crew:</strong> {details["crew"]}</p>
#         </div>
#         """, unsafe_allow_html=True)

# # 💬 Chat Interface
# with col2:
#     st.subheader("💬 Chat with Assistant")

#     # Display chat history
#     for role, msg in st.session_state.chat_history:
#         if role == "user":
#             st.markdown(f'<div class="user-msg"><strong>You:</strong> {msg}</div>', unsafe_allow_html=True)
#         else:
#             st.markdown(f'<div class="bot-msg"><strong>Agent:</strong><br>{msg}</div>', unsafe_allow_html=True)

#     # User input
#     with st.form("chat_form", clear_on_submit=True):
#         user_input = st.text_input("Your Message:")
#         submitted = st.form_submit_button("Send")

#     if submitted and user_input.strip():
#         st.session_state.chat_history.append(("user", user_input))

#         # Send message to Azure AI Agent
#         project.agents.messages.create(
#             thread_id=st.session_state.thread_id,
#             role="user",
#             content=user_input
#         )

#         run = project.agents.runs.create_and_process(
#             thread_id=st.session_state.thread_id,
#             agent_id=agent.id
#         )

#         with st.spinner("Agent is thinking..."):
#             timeout = 30
#             start = time.time()
#             while run.status in ["queued", "in_progress"]:
#                 if time.time() - start > timeout:
#                     break
#                 time.sleep(1)
#                 run = project.agents.runs.get(thread_id=st.session_state.thread_id, run_id=run.id)

#         # Get assistant response
#         if run.status == "failed":
#             st.session_state.chat_history.append(("agent", f"❌ Error: {run.last_error.get('message')}"))
#         else:
#             messages = project.agents.messages.list(
#                 thread_id=st.session_state.thread_id,
#                 order=ListSortOrder.ASCENDING
#             )

#             assistant_msgs = [m for m in messages if m.role == "assistant" and m.text_messages]
#             if assistant_msgs:
#                 last_msg = assistant_msgs[-1].text_messages[-1].text.value
#                 st.session_state.chat_history.append(("agent", last_msg))


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
        .chatbox { border: 1px solid #ccc; border-radius: 6px; padding: 15px; background: #ffffff; height: 400px; overflow-y: auto; }
        .user-msg { color: #003366; margin-bottom: 10px; }
        .bot-msg { color: #006400; margin-bottom: 20px; }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------
# Header
# ---------------------
st.markdown(
    '<div class="header"><img src="https://upload.wikimedia.org/wikipedia/commons/7/7e/Liberty_Mutual_Insurance_logo.svg"><h1>Liberty Work Order Assistant</h1></div>',
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
