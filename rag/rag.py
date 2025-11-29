### THIS WILL BE A TERMINAL VERSION FOR NOW ####
from langchain_classic.schema import Document
import re
import requests
from typing import Optional
from constants import LLM_TXT_PATTERN, LLM_TXT_URL_PATTERN
import logging


# CreateStore
import os
from typing import Optional
from models import embedding_model
from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings


logger = logging.getLogger(__name__)


class LoadLLMtxt:

    def __init__(self, url):
        self.url = url

    def urlContentLoader(self) -> Optional[requests.Response]:
        pattern = LLM_TXT_URL_PATTERN
        if not re.fullmatch(pattern, self.url):
            return None
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException:
            return None

    def llmtxtToDocuments(self) -> list[Document]:
        response = self.urlContentLoader()
        if response is None:
            return []

        raw_lines_unformatted = response.text.splitlines()
        raw_lines_formatted = [line.strip()
                               for line in raw_lines_unformatted if line.strip()]
        pattern = LLM_TXT_PATTERN
        documents: list[Document] = []

        for line in raw_lines_formatted:

            match = re.match(pattern, line)
            if not match:
                # print(f"⚠️ Skipped unparsable line:\n {line}")
                continue
            # make sure to add the group names in constants.py
            name = match.group("name")
            link = match.group("link")
            # TODO: fetch the description from the link using the mintlify format.
            description = match.group("description") or ""

            documents.append(Document(
                page_content=f"Name: {name}\nDescription: {description}\nLink: {link}",
                metadata={
                    "name": name,
                    "link": link
                }
            ))
        return documents

    def load(self):
        docs = self.llmtxtToDocuments()
        if not docs:
            logger.warning("No valid data found or failed to fetch URL.")
            return []
        logger.info(f"Loaded {len(docs)} entries.")
        return docs


class CreateStore:
    def __init__(self, documents: list[Document], embedding_model: Embeddings):
        self.documents = documents
        self.embedding_model = embedding_model

    def create(self, path: Optional[str] = None) -> FAISS:
        store = FAISS.from_documents(
            documents=self.documents,
            embedding=self.embedding_model
        )
        if path is not None:
            store.save_local(path)
        return store

    @staticmethod
    def loadStore(path: str, embedding_model: Embeddings) -> Optional[FAISS]:
        if os.path.exists(path):
            return FAISS.load_local(path, embedding_model, allow_dangerous_deserialization=True)
        logger.warning(f"Store not found at {path}")
        return None



# loader = LoadLLMtxt("https://docs.chainlit.io/llms.txt")
# docs = loader.load()
# vector_store = CreateStore(docs, embedding_model).create()

