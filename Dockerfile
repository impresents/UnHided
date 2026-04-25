FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install mediaflow-proxy

EXPOSE 7860

ENV PORT=7860

CMD ["uvicorn", "mediaflow_proxy.main:app", "--host", "0.0.0.0", "--port", "7860"]
