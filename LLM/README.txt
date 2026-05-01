# This should work for running a container for OLLAM.  
#	Flash Attention = 0: Prevents the "nil" runner crashes on the 1070.
#	Keep Alive = -1: Keeps the model in VRAM so you don't wait for a reload.
#	Num Thread 8: Maxes out your Haswell CPU’s ability to feed the GPU.
#	Num Ctx 4096: Keeps the VRAM usage at ~5.1 GB, avoiding the 7.2 GB "slowness" wall.

docker stop ollama && docker rm ollama

docker run -d --gpus=all \
  --name ollama \
  -v ollama:/root/.ollama \
  -v $(pwd):/modelfiles \
  -e OLLAMA_HOST=0.0.0.0 \
  -p 11434:11434 \
  -e OLLAMA_FLASH_ATTENTION=1 \
  -e OLLAMA_KEEP_ALIVE=-1\
  ollama/ollama

# TO use the mistral LM....  Takes about 5GB vram and is pretty smart and quick
# Dump this into a file (mistral_v0.3.modelfile)
FROM mistral:v0.3
# Hardware-specific tunables for Haswell/Pascal
PARAMETER num_ctx 4096
PARAMETER num_thread 8

# Personal Identity
SYSTEM """
You are a Principal AI Architect and property owner in Canyon County. 
Focus on surgical accuracy and simplifying complex technical/zoning problems.
"""

# Build the container
docker exec -it ollama ollama create mistral-rre -f /modelfiles/mistral_v0.3.modelfile

# Run the LLM
docker exec -it ollama ollama run mistral-ranch
