import base64
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_URL_AUTH = 'https://accounts.spotify.com/authorize/?'
SPOTIFY_URL_TOKEN = 'https://accounts.spotify.com/api/token/'

CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")

# Port and callback url can be changed or ledt to localhost:5000
PORT = "5000"
CALLBACK_URL = "http://localhost"
REDIRECT_URI = os.environ.get("SPOTIPY_REDIRECT_URI")

# Add needed scope from spotify user (TODO: revisit this)
# https://developer.spotify.com/documentation/web-api/concepts/scopes
SCOPE = "user-read-private user-read-email user-library-read playlist-read-private"
# SCOPE = "streaming user-read-birthdate user-read-email user-read-private"


def get_spotify_auth_url():
    url = "{0}client_id={1}&response_type=code&redirect_uri={2}&scope={3}".format(
        SPOTIFY_URL_AUTH,
        CLIENT_ID,
        REDIRECT_URI,
        SCOPE
    )
    return url


def get_token(code):
    body = {
        "grant_type": 'client_credentials',
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    id_secret = "{}:{}".format(CLIENT_ID, CLIENT_SECRET)
    encoded_bytes = base64.b64encode(id_secret.encode('utf-8'))
    headers = {
        "Content-Type": 'application/x-www-form-urlencoded',
        "Authorization": f"Basic {encoded_bytes.decode('utf-8')}"
    }

    post = requests.post(SPOTIFY_URL_TOKEN, params=body, headers=headers)
    response = json.loads(post.text)
    access_token = response.get("access_token")
    return access_token
