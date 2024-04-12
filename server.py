import spotipy
from flask import Flask, render_template, redirect, request
import requests
import spotify_auth



app = Flask(__name__)
access_token = None


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
    # 1. get code from URL and extract access token
    access_token = spotify_auth.get_token(request.args.get('code'))
    return {
        "access_token": access_token,
        "message": "Navigate to homepage (http://localhost:5000) to see actual data now that you have an"
    }


@app.route('/track')
def get_track():
    track_id = '2TpxZ7JUBn3uw46aR7qd6V'
    if access_token is None:
        return redirect('/spotify-login')
    else:
        headers = {"Authorization": f"Bearer {access_token}"}
        url = f'https://api.spotify.com/v1/tracks/{track_id}'
        data = requests.get(url, headers=headers)
        return data.json()


@app.route('/playlists')
def get_user_playlists():
    if access_token is None:
        return redirect('/spotify-login')
    else:
        sp = spotipy.Spotify(auth=access_token)
        playlists = sp.user_playlists('vanwars')
        return playlists


# @app.route('/user')
# def get_user():
#     if access_token is None:
#         return redirect('/spotify-login')
#     else:
#         sp = spotipy.Spotify(auth=access_token)
#         user = sp.current_user()
#         return user


@app.route('/user')
def get_user():
    if access_token is None:
        return redirect('/spotify-login')
    else:
        headers = {"Authorization": f"Bearer {access_token}"}
        url = f'https://api.spotify.com/v1/me'
        data = requests.get(url, headers=headers)
        return data.json()
