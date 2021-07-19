FROM python:3.8-slim-buster

ENV LISTEN_PORT=5000

EXPOSE 5000

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0"]