FROM python:3.8.10

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY . .
# 시스템 패키지 업데이트
RUN apt-get update
RUN apt-get upgrade
RUN apt install libgl1-mesa-glx
RUN pip install --upgrade pip
RUN pip install -r requirements.txt