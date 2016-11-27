FROM python:2.7

ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt
EXPOSE 5000

ENTRYPOINT python app/app.py --host=0.0.0.0
