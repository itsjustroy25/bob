#!/bin/bash
# Wait for Docker to be ready
MAX_WAIT=180
WAITED=0
until docker ps > /dev/null 2>&1; do
	sleep 5
	WAITED=$((WAITED + 5))
	if [ $WAITED -ge $MAX_WAIT ]; then
		echo "[$(date)] Docker never became ready after ${MAX_WAIT}s, giving up." >> /home/rleach/bob/watchdog.log
		exit 1
	fi
done
echo "[$(date)] Docker ready after ${WAITED}s" >> /home/rleach/bob/watchdog.log

echo "Starting ollama..."
docker start ollama

echo "Waiting for ollama to be ready..."
until curl -s http://localhost:11434/api/tags > /dev/null 2>&1; do
	    sleep 5
    done
    echo "Ollama is ready."

    echo "Loading Bob into VRAM..."
docker exec ollama ollama run bob "wake up" > /dev/null 2>&1
echo "Bob loaded."

docker start bob-flask
sleep 5
docker start bob-nginx
sleep 5
sudo service cloudflared start

echo "All services started."

# Start watchdog
pkill -f watchdog.sh 2>/dev/null
nohup /home/rleach/bob/watchdog.sh > /dev/null 2>&1 &
echo "Watchdog started."

#!docker start ollama
#sleep 60
#docker start bob-flask
#sleep 5
#docker start bob-nginx
#sleep 5
#sudo service cloudflared start
