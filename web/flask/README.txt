# to build:
docker build -f flask.dockerfile -t bob-flask .

# to run:
docker run -d --name bob-flask -p 5000:5000 -v /home/rleach/bob/web/flask/static:/app/static bob-flask
