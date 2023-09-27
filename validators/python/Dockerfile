FROM python:3.11-bullseye

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN chmod +x validator-and-generator.py

RUN ln --symbolic /app/validator-and-generator.py /usr/bin/si-validator