import streamlit as st
import requests

API_BASE = "https://fey1agm25l.execute-api.ap-south-1.amazonaws.com/dev"

st.set_page_config(page_title="Assistant Manager", layout="centered")

st.title("🧠 Pinecone Assistant Manager")


# ========== 1. Create Assistant ==========
st.header("1️⃣ Create Assistant")

with st.form("create_form"):
    assistant_name = st.text_input("Assistant Name", key="assistant")
    zip_file = st.file_uploader("Upload ZIP File (PDFs inside)", type="zip")
    create_btn = st.form_submit_button("🚀 Create Assistant")

if create_btn and zip_file and assistant_name:
    files = {
        "zip_file": (zip_file.name, zip_file, "application/zip"),
    }
    data = {"assistant_name": assistant_name}
    res = requests.post(f"{API_BASE}/create-assistant", files=files, data=data)
    st.success(res.json().get("message")) if res.ok else st.error(res.text)


# ========== 2. Query Assistant ==========
st.header("2️⃣ Query Assistant")

with st.form("query_form"):
    q_assistant = st.text_input("Assistant Name", key="query_asst")
    query_text = st.text_area("Your Question")
    query_btn = st.form_submit_button("💬 Ask")

if query_btn and q_assistant and query_text:
    payload = {
        "assistant_name": q_assistant,
        "query": query_text
    }
    res = requests.post(f"{API_BASE}/query-assistant", json=payload)
    if res.ok:
        st.markdown("**Answer:**")
        st.success(res.json().get("response"))
    else:
        st.error(res.text)


# ========== 3. Delete Assistant ==========
st.header("3️⃣ Delete Assistant")

with st.form("delete_form"):
    del_assistant = st.text_input("Assistant Name to Delete", key="delete_asst")
    delete_btn = st.form_submit_button("🗑️ Delete")

if delete_btn and del_assistant:
    payload = {"assistant_name": del_assistant}
    res = requests.post(f"{API_BASE}/delete-assistant", json=payload)
    st.success(res.json().get("message")) if res.ok else st.error(res.text)
