from flask import Flask, redirect, request
import subprocess

app = Flask(__name__)

@app.route("/live")
def live():
    url = request.args.get("url")
    if not url:
        return "url parametresi eksik", 400
    try:
        result = subprocess.check_output(
            ["yt-dlp", "-g", "--no-playlist", "-f", "best", url],
            stderr=subprocess.STDOUT,
            timeout=30
        ).decode().strip()
        lines = result.split("\n")
        # Son satır URL, öncekiler log
        stream_url = lines[-1]
        return redirect(stream_url)
    except subprocess.CalledProcessError as e:
        return e.output.decode(), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
