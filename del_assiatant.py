# delete_assistant.py
from pinecone import Pinecone

# Replace with your actual Pinecone API Key
API_KEY = "pcsk_w9Hxy_5x4QjXh7o17b2iGpdPGTGUDYiMbD6KAgJitQtucLUVL7tk9ckkDDSevoFZNECjq"
ASSISTANT_NAME = "project-summary-assistant"  # Change if needed

# Initialize Pinecone
pc = Pinecone(api_key=API_KEY)

# Delete the assistant
try:
    pc.assistant.delete_assistant(assistant_name=ASSISTANT_NAME)
    print(f"[✓] Assistant '{ASSISTANT_NAME}' deleted successfully.")
except Exception as e:
    print(f"[!] Failed to delete assistant: {e}")
