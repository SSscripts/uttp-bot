from flask import Flask, redirect, request, session
from google_auth_oauthlib.flow import Flow
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

CLIENT_ID = "836408101082-1phe0vcm833p2o16vg2vevvco6r2q2ev.apps.googleusercontent.com"
REDIRECT_URI = "https://uttp-bot.onrender.com/oauth2callback"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

flow = Flow.from_client_config(
    {
        "web": {
            "client_id": CLIENT_ID,
            "project_id": "uttp-bot",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [REDIRECT_URI],
            "client_secret": os.getenv("CLIENT_SECRET")
        }
    },
    scopes=SCOPES,
    redirect_uri=REDIRECT_URI
)

@app.route("/")
def index():
    auth_url, _ = flow.authorization_url(prompt='consent')
    return redirect(auth_url)

@app.route("/oauth2callback")
def oauth2callback():
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    session['token'] = credentials.token
    return "✅ YouTube account connected! (Filtering system coming next...)"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
