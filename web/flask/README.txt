# to clear credentials:
rm ~/.docker/config.json
mkdir -p ~/.docker
echo '{"credsStore": ""}' > ~/.docker/config.json
docker login -u itsjustroy

# to build:
docker build -f flask.dockerfile -t bob-flask .

# to run:
docker run -d --name bob-flask -p 5000:5000 -v /home/rleach/bob/web/flask/static:/app/static bob-flask
