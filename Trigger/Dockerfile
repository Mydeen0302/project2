FROM python:3.10-slim

WORKDIR /app

COPY trigger.py .

RUN pip install --no-cache-dir requests

CMD ["python3", "trigger.py"]
