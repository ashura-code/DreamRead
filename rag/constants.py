LLM_MODEL = "llama-3.3-70b-versatile"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_TXT_URL_PATTERN = r"https?://.*llms\.txt$"
LLM_TXT_PATTERN = r'- \[(?P<name>.*?)\]\((?P<link>.*?)\)(?:: (?P<description>.*))?'
