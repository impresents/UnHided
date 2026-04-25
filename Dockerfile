FROM python:3.11-slim

WORKDIR /app

RUN pip install flask yt-dlp

COPY run.py .

EXPOSE 7860

CMD ["python", "run.py"]
