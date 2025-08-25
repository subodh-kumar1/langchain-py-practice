import os
from dotenv import load_dotenv

load_dotenv()  # This is necessary to load the .env file

OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MAX_RETRIES = os.getenv("MAX_RETRIES")
ES_URL = os.getenv("ES_URL")
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL")
GIT_LOCAL_DIR=os.getenv("GIT_LOCAL_DIR")
GIT_REPO_URL=os.getenv("GIT_REPO_URL")
INDEX_NAME=os.getenv("INDEX_NAME")
RECORD_MANAGER_DB=os.getenv("RECORD_MANAGER_DB")

print(OPENAI_API_KEY)
print(OPENAI_EMBEDDING_MODEL)
print(MAX_RETRIES)
print(ES_URL)
print(GIT_LOCAL_DIR)
print(GIT_REPO_URL)
print(INDEX_NAME)
print(RECORD_MANAGER_DB)

