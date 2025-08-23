FROM python:3.8-slim-buster

WORKDIR /flask

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=run.py
ENV FLASK_ENV=development

CMD ["python3", "run.py"]
