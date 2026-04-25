from flask import Flask, redirect, request
import subprocess, os, tempfile

app = Flask(__name__)

@app.route("/live")
def live():
    url = request.args.get("url")
    if not url:
        return "url parametresi eksik", 400
    try:
        cookies = os.environ.get("YOUTUBE_COOKIES", "")
        cmd = ["yt-dlp", "-g", "--no-playlist", "-f", "b", url]
        if cookies:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
                f.write(cookies)
                cmd += ["--cookies", f.name]
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=30).decode().strip()
        stream_url = result.split("\n")[-1]
        return redirect(stream_url)
    except subprocess.CalledProcessError as e:
        return e.output.decode(), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
