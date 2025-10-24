FROM python:3.11-slim
WORKDIR /app

COPY . /app

RUN python3 -m pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1
CMD ["python", "-m", "pipelines.daily_runner"]
