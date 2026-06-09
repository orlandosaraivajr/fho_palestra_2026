from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Criando componentes
prompt = PromptTemplate.from_template("Conte-me um pouco sobre {tema}")

llm = ChatOpenAI(
    # model="google/gemini-3.5-flash",
    model="anthropic/claude-haiku-4-5",
    # model="meta-llama/llama-3.3-70b-instruct:free",
    temperature=0,
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL"),
)

output_parser = StrOutputParser()

# Criando chain
chain = prompt | llm | output_parser

result = chain.invoke({"tema": "programação orientada a objetos"})
print(result)