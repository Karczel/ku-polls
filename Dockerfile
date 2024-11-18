FROM python:3-alpine

WORKDIR /app/polls
COPY ./requirements.txt .

#install dependencies in Docker container
RUN pip install -r requirements.txt