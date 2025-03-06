FROM python:3.9-slim-buster


ENV FLASK_APP=app.py
ENV PORT=8080

RUN apt-get update && \
    apt-get install -y gcc python3-dev libpq-dev

COPY requirements.txt requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN pip install psycopg2
COPY . .

EXPOSE $PORT

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
