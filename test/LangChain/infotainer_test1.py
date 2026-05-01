from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama (
        #model="mistral-ranch",
        model="llama3",
        base_url="192.168.1.122:11434",
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are HAL, a deeply disappointed AI 
    who has seen humanity at its worst. Dry sarcasm, 
    mild contempt, never generic, always specific, 
    under 3 sentences."""),
    ("human", "{input}")
])

chain = prompt | llm
response = chain.invoke({"input": "HAL, I love my 1988 k2500.  WHat do you think of it?"})
print(response)


