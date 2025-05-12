import streamlit as st
import requests

# Use the exact endpoint from your API Gateway screenshot
API_BASE = "https://fey1agm2SI.execute-api.ap-south-1.amazonaws.com/dev"

st.title("📚 Document-based Assistant Manager")

menu = st.sidebar.radio("Choose Action", ["Create Assistant", "Query Assistant", "Delete Assistant"])

# 1. CREATE ASSISTANT
if menu == "Create Assistant":
    st.header("🔧 Create Assistant")
    assistant_name = st.text_input("Assistant Name")
    
    if st.button("Create"):
        if assistant_name:
            res = requests.post(
                f"{API_BASE}/create-assistant",
                json={"assistant_name": assistant_name}
            )
            if res.status_code == 200:
                st.success(res.json().get("message"))
            else:
                st.error(f"❌ Error: {res.text}")
        else:
            st.warning("Assistant name required")

# 2. QUERY ASSISTANT
elif menu == "Query Assistant":
    st.header("💬 Query Assistant")
    assistant_name = st.text_input("Assistant Name")
    query = st.text_area("Your Question")

    if st.button("Ask"):
        if assistant_name and query:
            res = requests.post(
                f"{API_BASE}/query-assistant",
                json={"assistant_name": assistant_name, "query": query}
            )
            if res.status_code == 200:
                st.success(res.json().get("response"))
            else:
                st.error(f"❌ Error: {res.text}")
        else:
            st.warning("Both fields are required")

# 3. DELETE ASSISTANT
elif menu == "Delete Assistant":
    st.header("🗑️ Delete Assistant")
    assistant_name = st.text_input("Assistant Name to Delete")

    if st.button("Delete"):
        if assistant_name:
            res = requests.post(
                f"{API_BASE}/delete-assistant",
                json={"assistant_name": assistant_name}
            )
            if res.status_code == 200:
                st.success(res.json().get("message"))
            else:
                st.error(f"❌ Error: {res.text}")
        else:
            st.warning("Assistant name required")