from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message
import os
import zipfile

# ====== Step 1: Unzip your project summary ZIP ======
zip_path = r"C:\Users\navne\Downloads\Git\sign4l\Project_Summary.zip"
extract_dir = r"C:\Users\navne\Downloads\Git\sign4l\unzipped"

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)
print("[✓] Unzipped all PDFs.")


# ====== Step 2: Initialize Pinecone Assistant ======
API_KEY = "pcsk_w9Hxy_5x4QjXh7o17b2iGpdPGTGUDYiMbD6KAgJitQtucLUVL7tk9ckkDDSevoFZNECjq"
pc = Pinecone(api_key=API_KEY)

# Only run ONCE to create the assistant. You can comment this out after the first run.
try:
    assistant = pc.assistant.create_assistant(
        assistant_name="project-summary-assistant",
        instructions="Answer based only on the documents provided. Use clear American English.",
        region="us",
        timeout=30
    )
    print("[✓] Assistant created.")
except Exception as e:
    print("[!] Assistant may already exist. Skipping creation.")


# ====== Step 3: Upload PDFs to Assistant ======
assistant = pc.assistant.Assistant(assistant_name="project-summary-assistant")

for filename in os.listdir(extract_dir):
    if filename.lower().endswith(".pdf"):
        file_path = os.path.join(extract_dir, filename)
        print(f"[~] Uploading: {file_path}")
        response = assistant.upload_file(
            file_path=file_path,
            metadata={"project_type": "summaries", "source": "unzipped_pdf"},
            timeout=None
        )
print("[✓] All PDF files uploaded.")


# ====== Step 4: Ask a question and get a clean answer ======
msg = Message(role="user", content="Cloud Migration Initiative")
resp = assistant.chat(messages=[msg])

# Clean answer
clean_answer = resp['message']['content']
print(f"\n[✅ Answer]\n{clean_answer}")
