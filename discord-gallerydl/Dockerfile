FROM python:3.9-alpine

RUN pip install --upgrade pip
RUN apk add  --no-cache ffmpeg

WORKDIR /dgdl

COPY requirements.txt .
RUN pip install -r requirements.txt

USER 1000
COPY start.py .
COPY app app

CMD [ "python", "start.py" ]