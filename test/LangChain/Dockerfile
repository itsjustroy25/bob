# Use a slim Python image to keep the "bloat" low
FROM python:3.11-slim

WORKDIR /app

# Install the core LangChain and Ollama integration
RUN pip install --no-cache-dir \
    langchain \
    langchain-ollama \
    langchain-community

# Keep the container running so you can 'exec' into it
CMD ["tail", "-f", "/dev/null"]
