FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install psycopg2-binary
RUN pip install -r requirements.txt


COPY . .

# EXPOSE 8000