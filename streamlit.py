import streamlit as st
import requests

API_BASE = "https://fey1agm25l.execute-api.ap-south-1.amazonaws.com/dev"
API_KEY = "demoHub"

headers = {
    "x-api-key": API_KEY  # API Key header
}

st.title("📚 Document-based Assistant Manager")

menu = st.sidebar.radio("Choose Action", ["Create Assistant", "Query Assistant", "Delete Assistant"])

# 1. CREATE ASSISTANT
if menu == "Create Assistant":
    st.header("🔧 Create Assistant & Upload ZIP")
    assistant_name = st.text_input("Assistant Name")
    zip_file = st.file_uploader("Upload ZIP file of PDFs", type=["zip"])

    if st.button("Create and Upload"):
        if assistant_name and zip_file:
            files = {
                "zip_file": zip_file,
            }
            data = {
                "assistant_name": assistant_name
            }
            res = requests.post(f"{API_BASE}/create-assistant", files=files, data=data, headers=headers)
            if res.ok:
                st.success(res.json().get("message"))
            else:
                st.error(f"❌ Error: {res.text}")
        else:
            st.warning("Please enter an assistant name and upload a ZIP file.")

# 2. QUERY ASSISTANT
elif menu == "Query Assistant":
    st.header("💬 Query Assistant")
    assistant_name = st.text_input("Assistant Name")
    query = st.text_area("Ask a question")

    if st.button("Ask"):
        if assistant_name and query:
            payload = {
                "assistant_name": assistant_name,
                "query": query
            }
            res = requests.post(f"{API_BASE}/query-assistant", json=payload, headers=headers)
            if res.ok:
                st.success(res.json().get("response"))
            else:
                st.error(f"❌ Error: {res.text}")
        else:
            st.warning("Enter both assistant name and query.")

# 3. DELETE ASSISTANT
elif menu == "Delete Assistant":
    st.header("🗑️ Delete Assistant")
    assistant_name = st.text_input("Assistant Name to Delete")

    if st.button("Delete"):
        if assistant_name:
            payload = {
                "assistant_name": assistant_name
            }
            res = requests.post(f"{API_BASE}/delete-assistant", json=payload, headers=headers)
            if res.ok:
                st.success(res.json().get("message"))
            else:
                st.error(f"❌ Error: {res.text}")
        else:
            st.warning("Enter an assistant name to delete.")
