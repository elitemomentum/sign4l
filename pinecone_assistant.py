# upload_docs.py
from pinecone import Pinecone
import os
import zipfile

# ====== Step 1: Unzip ZIP ======
zip_path = r"C:\Users\navne\Downloads\Git\sign4l\Project_Summary.zip"
extract_dir = r"C:\Users\navne\Downloads\Git\sign4l\unzipped"

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)
print("[✓] Unzipped all PDFs.")

# ====== Step 2: Initialize Pinecone ======
API_KEY = "pcsk_w9Hxy_5x4QjXh7o17b2iGpdPGTGUDYiMbD6KAgJitQtucLUVL7tk9ckkDDSevoFZNECjq"
pc = Pinecone(api_key=API_KEY)

# Create assistant (only once)
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

# ====== Step 3: Upload PDFs ======
assistant = pc.assistant.Assistant(assistant_name="project-summary-assistant")

for filename in os.listdir(extract_dir):
    if filename.lower().endswith(".pdf"):
        file_path = os.path.join(extract_dir, filename)
        print(f"[~] Uploading: {file_path}")
        assistant.upload_file(
            file_path=file_path,
            metadata={"project_type": "summaries", "source": "unzipped_pdf"},
            timeout=None
        )
print("[✓] Upload complete.")
