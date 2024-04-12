# configuration
poetry new playlist-app
cd playlist-app
poetry add flask
poetry add requests


# running flask
export FLASK_APP=server.py
poetry run flask run --debug