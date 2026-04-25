from flask import Flask, redirect, request
import subprocess

app = Flask(__name__)

@app.route("/live")
def live():
    url = request.args.get("url")
    password = request.args.get("api_password")
    if not url:
        return "url parametresi eksik", 400
    try:
        result = subprocess.check_output(
            ["yt-dlp", "-g", "--no-playlist", url],
            timeout=30
        ).decode().strip().split("\n")[0]
        return redirect(result)
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
