from flask import Flask, redirect, request, jsonify
import requests

app = Flask(__name__)

API_BASE = "https://core-api.kablowebtv.com/api"

FIREBASE_API_KEY = "AIzaSyBvHxNGNqP8Q7zA3M6JkXvwQkXJPkFzRtY"  # firebase key

TVH_EMAIL = "EMAIL"      # tvheryerde emailin
TVH_PASSWORD = "SIFRE"   # tvheryerde şifren

def get_token():
    # Firebase login
    r = requests.post(
        f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}",
        json={"email": TVH_EMAIL, "password": TVH_PASSWORD, "returnSecureToken": True}
    )
    firebase_token = r.json()["idToken"]
    
    # kablowebtv login
    r2 = requests.post(
        f"{API_BASE}/auth/login",
        json={"firebaseToken": firebase_token},
        headers={"Content-Type": "application/json"}
    )
    return r2.json()["Data"]["Token"]

def get_stream(channel_uid, token):
    r = requests.get(
        f"{API_BASE}/channels/detail?channelUId={channel_uid}",
        headers={"Authorization": f"Bearer {token}"}
    )
    return r.json()["Data"]["StreamData"]["HlsStreamUrl"]

@app.route("/live/<channel_uid>")
def live(channel_uid):
    try:
        token = get_token()
        url = get_stream(channel_uid, token)
        return redirect(url)
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
