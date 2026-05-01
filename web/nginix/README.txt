cd ~/bob/web/nginx
docker build -f nginx.dockerfile -t bob-nginx .
docker run -d \
  --name bob-nginx \
  -p 80:80 \
  bob-nginx
