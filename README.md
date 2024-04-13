# Configuration

## Clone and add dependencies
```bash
git clone https://github.com/vanwars/playlist-app.git
cd playlist-app
poetry install
```

## Create Environment Variable File
In the root of your `name-of-app` folder, create a secret file called `.env` (that you'll exclude from version control). In it, paste your application keys, which will set some environment variables when your application starts up:

```bash
SPOTIFY_CLIENT_ID='YOUR_CLIENT_ID'
SPOTIFY_CLIENT_SECRET='YOUR_CLIENT_SECRET'
SPOTIFY_REDIRECT_URI='http://localhost:5000/callback'
FLASK_APP=server.py
```

# Running Flask 
From the command line, run this command:
```bash
poetry run flask run --debug
```
The `--debug` flag will enable hot reloading when you make changes to your code.