# syntax=docker/dockerfile:1
FROM python:latest
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python3",  "run.py"]
EXPOSE 5000