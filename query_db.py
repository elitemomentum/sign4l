# query_db.py
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message

# ====== Step 1: Initialize Pinecone Assistant ======
API_KEY = "pcsk_w9Hxy_5x4QjXh7o17b2iGpdPGTGUDYiMbD6KAgJitQtucLUVL7tk9ckkDDSevoFZNECjq"
pc = Pinecone(api_key=API_KEY)
assistant = pc.assistant.Assistant(assistant_name="project-summary-assistant")

# ====== Step 2: Ask your question ======
query = input("Ask your question: ")
msg = Message(role="user", content=query)
resp = assistant.chat(messages=[msg])

# Clean answer
clean_answer = resp['message']['content']
print(f"\n[✅ Answer]\n{clean_answer}")