from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from constants import LLM_MODEL, EMBEDDING_MODEL
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model=LLM_MODEL,
    temperature=0.3,
    max_tokens=4096,
    timeout=30,  # seconds
    max_retries=2,
    api_key=os.getenv("GROK_API_KEY")
)

embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
