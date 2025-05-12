import streamlit as st
import requests
import os

# Configuration
API_BASE = os.getenv("API_BASE", "https://fey1agm2SI.execute-api.ap-south-1.amazonaws.com/dev")
USE_S3 = True  # Set to False if you want to upload files directly

st.title("📚 Document-based Assistant Manager")

# Initialize session state
if 'assistant_name' not in st.session_state:
    st.session_state.assistant_name = ""

# Sidebar menu
menu = st.sidebar.radio("Choose Action", ["Create Assistant", "Query Assistant", "Delete Assistant"])

def make_api_call(endpoint, payload):
    try:
        response = requests.post(
            f"{API_BASE}/{endpoint}",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

# 1. CREATE ASSISTANT
if menu == "Create Assistant":
    st.header("🔧 Create Assistant")
    st.session_state.assistant_name = st.text_input("Assistant Name", value=st.session_state.assistant_name)
    
    if not USE_S3:
        uploaded_files = st.file_uploader(
            "Upload PDF Documents",
            type=["pdf"],
            accept_multiple_files=True
        )
    
    if st.button("Create Assistant"):
        if st.session_state.assistant_name:
            payload = {
                "assistant_name": st.session_state.assistant_name
            }
            
            result = make_api_call("create-assistant", payload)
            
            if result:
                if result.get("status") == "success":
                    st.success(f"Assistant created! {result.get('message')}")
                else:
                    st.warning(result.get("message", "Assistant creation completed with warnings"))
        else:
            st.warning("Please enter an assistant name")

# 2. QUERY ASSISTANT
elif menu == "Query Assistant":
    st.header("💬 Query Assistant")
    assistant_name = st.text_input("Assistant Name", value=st.session_state.assistant_name)
    query = st.text_area("Your Question", height=150)
    
    if st.button("Ask Question"):
        if assistant_name and query:
            payload = {
                "assistant_name": assistant_name,
                "query": query
            }
            
            result = make_api_call("query-assistant", payload)
            
            if result:
                st.subheader("Response")
                st.markdown(f"```\n{result.get('response', 'No response')}\n```")
        else:
            st.warning("Both assistant name and question are required")

# 3. DELETE ASSISTANT
elif menu == "Delete Assistant":
    st.header("🗑️ Delete Assistant")
    assistant_name = st.text_input("Assistant Name to Delete", value=st.session_state.assistant_name)
    
    if st.button("Delete Assistant", type="primary"):
        if assistant_name:
            payload = {
                "assistant_name": assistant_name
            }
            
            result = make_api_call("delete-assistant", payload)
            
            if result:
                if result.get("status") == "success":
                    st.success(result.get("message"))
                    st.session_state.assistant_name = ""
                else:
                    st.error(result.get("message", "Deletion failed"))
        else:
            st.warning("Please enter an assistant name")

# Connection troubleshooting
st.sidebar.markdown("---")
if st.sidebar.button("Test API Connection"):
    try:
        test_response = requests.get(API_BASE, timeout=5)
        if test_response.status_code == 403:  # Common API Gateway response
            st.sidebar.success("✅ API Endpoint reachable")
        else:
            st.sidebar.warning(f"⚠️ Unexpected response: {test_response.status_code}")
    except Exception as e:
        st.sidebar.error(f"❌ Connection failed: {str(e)}")
        st.sidebar.markdown(f"Trying to reach: `{API_BASE}`")