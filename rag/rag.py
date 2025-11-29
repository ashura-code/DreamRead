### THIS WILL BE A TERMINAL VERSION FOR NOW ####
from langchain_classic.schema import Document
import re
import requests
from typing import Optional
from constants import LLM_TXT_PATTERN, LLM_TXT_URL_PATTERN
import logging

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
                page_content=name+","+description+","+link,
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


loader = LoadLLMtxt("https://docs.chainlit.io/llms.txt")
print(loader.load()[0])
