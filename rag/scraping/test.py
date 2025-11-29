import requests
from langchain_classic.schema import Document
from langchain_community.vectorstores import FAISS
from models import embedding_model
import re


CHAINLIT_LLM_LIST_URL = "https://docs.chainlit.io/llms.txt"

response = requests.get(CHAINLIT_LLM_LIST_URL)
response.raise_for_status()  # Fail fast if request fails

raw_lines = response.text.splitlines()
raw_lines = [line.strip() for line in raw_lines if line.strip()]

# Description is optional `(?:: (.*))?`
ITEM_PATTERN = r'- \[(?P<name>.*?)\]\((?P<link>.*?)\)(?:: (?P<description>.*))?'

documents: list[Document] = []

for line in raw_lines:
    match = re.match(ITEM_PATTERN, line)
    if not match:
        print(f"⚠️ Skipped unparsable line:\n {line}")
        continue

    name = match.group("name")
    link = match.group("link")
    description = match.group("description") or ""

    documents.append(
        Document(
            page_content=description,
            metadata={
                "name": name,
                "url": link,
                "description": description
            }
        )
    )


vector_store = FAISS.from_documents(documents, embedding=embedding_model)
dim = vector_store.similarity_search("How can I use MCP in chainlit?")
print(dim)
