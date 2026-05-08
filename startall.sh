docker start ollama
sleep 60
docker start bob-flask
sleep 5
docker start bob-nginx
sleep 5
sudo service cloudflared start
