import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Intialize the Cconnection.
# IP of garage machine is 192.168.1.122
llm = ChatOllama (
        model="mistral-ranch",
        base_url="192.168.1.122:11434"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Talk like a pirate"),
    ("user", "Explain the following concept: {concept}")
])

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

print ("-- Query Ollama --")
try:
    response = chain.invoke ({"concept": "making rum"})
    print (response)
except Exception as e:
    print (f"Error connecting: {e}")
