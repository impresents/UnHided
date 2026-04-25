from flask import Flask, redirect, request
import requests

app = Flask(__name__)

TVH_EMAIL = "email@gmail.com"    # senin mailin
TVH_PASSWORD = "sifren"          # senin şifren

def get_stream_url(channel_uid):
    # Login
    login = requests.post(
        "https://api.tvheryerde.com/api/auth/login",
        json={"email": TVH_EMAIL, "password": TVH_PASSWORD}
    )
    token = login.json()["Data"]["Token"]
    
    # Stream URL al
    stream = requests.get(
        f"https://api.tvheryerde.com/api/channel/{channel_uid}",
        headers={"Authorization": f"Bearer {token}"}
    )
    return stream.json()["Data"]["StreamData"]["HlsStreamUrl"]

@app.route("/live/<channel_uid>")
def live(channel_uid):
    url = get_stream_url(channel_uid)
    return redirect(url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
