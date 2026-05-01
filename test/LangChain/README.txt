# Run from WSL to spin up node specified in Dockerfile
docker build -t langchain-node .

docker run -d \
  --name ai-logic \
  -v $(pwd):/app \
  -e OLLAMA_BASE_URL="http://192.168.1.122:11434" \
  langchain-node
