from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from src.const import OPENAI_API_KEY, OPENAI_CHAT_MODEL

prompt_template = PromptTemplate.from_template("Tell me a {adjective} joke about {content}.")

prompt = prompt_template.format(adjective="funny", content="robots")

print(prompt)

llm = ChatOpenAI(model=OPENAI_CHAT_MODEL, max_retries=2, openai_api_key=OPENAI_API_KEY)

response = llm.invoke(prompt)

print(response)