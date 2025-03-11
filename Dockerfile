FROM python:3.10.1 as fastapi

WORKDIR /fastapi

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /fastapi/app

