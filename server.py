from flask import Flask, render_template, redirect, request
import requests
import spotify_auth


access_token = None
refresh_token = None
unauthorized_message = "You need to log in. Go to the login site and then try again: '/spotify-login."


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/spotify-login')
def login_spotify():
    response = spotify_auth.get_spotify_auth_url()
    print(response)
    return redirect(response)


@app.route('/callback/')
def process_token_spotify():
    global access_token
    global refresh_token
    # 1. get code from URL and extract access token
    credentials = spotify_auth.get_spotify_credentials(
        request.args.get('code'))

    access_token = credentials.get("access_token")
    refresh_token = credentials.get("refresh_token")
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "scope": credentials.get('expires_in'),
        "token_type": credentials.get("token_type"),
        "expires_in": credentials.get("expires_in"),
        "message": "Navigate to homepage (http://localhost:5000) to see actual data now that you have an"
    }


@app.route('/api/track')
def get_track():
    track_id = '2TpxZ7JUBn3uw46aR7qd6V'
    if access_token is None:
        return {'unauthorized': unauthorized_message}
    else:
        headers = {"Authorization": f"Bearer {access_token}"}
        url = f'https://api.spotify.com/v1/tracks/{track_id}'
        data = requests.get(url, headers=headers)
        return data.json()


@app.route('/api/playlists')
def get_user_playlists():
    if access_token is None:
        return {'unauthorized': unauthorized_message}
    else:
        headers = {"Authorization": f"Bearer {access_token}"}
        url = 'https://api.spotify.com/v1/me/playlists'
        data = requests.get(url, headers=headers)
        return data.json()


@app.route('/api/recently-played')
def get_recently_played():
    if access_token is None:
        return {'unauthorized': unauthorized_message}
    else:
        headers = {"Authorization": f"Bearer {access_token}"}
        url = 'https://api.spotify.com/v1/me/player/recently-played'
        data = requests.get(url, headers=headers)
        return data.json()


@app.route('/api/user')
def get_user():
    if access_token is None:
        return {'unauthorized': unauthorized_message}
    else:
        headers = {"Authorization": f"Bearer {access_token}"}
        url = 'https://api.spotify.com/v1/me'
        data = requests.get(url, headers=headers)
        return data.json()
