import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch
import langchain
langchain.debug = True
langchain.verbose = True

# Intialize the Cconnection.
# IP of garage machine is 192.168.1.122
llm = ChatOllama (
        model="mistral-ranch",
        base_url="192.168.1.122:11434",
)

classifier_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a routing engine. Classify the user input as either 'TIME' or 'Other'."),
        ("user", "{input}")
])

# We want to see just Time or Other
output_parser = StrOutputParser()

classifier = classifier_prompt | llm | output_parser

time_chain = ChatPromptTemplate.from_template ("Tell a joke about time:{input}") | llm | output_parser
general_chain = ChatPromptTemplate.from_template ("Respond normally:{input}") | llm | output_parser

router = RunnableBranch (
        ( lambda x: "TIME" in x["intent"].upper(), time_chain),
        general_chain # Default path
)

full_chain = (
        {"intent": classifier, "input": lambda x: x["input"]}
        | router
)
print ("-- Query Ollama --")
try:
    response = full_chain.invoke ({"input": "What time is it?"})
    print (response)
except Exception as e:
    print (f"Error connecting: {e}")
