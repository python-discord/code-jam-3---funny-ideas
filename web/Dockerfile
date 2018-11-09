FROM python:latest

COPY . /opt/app
WORKDIR /opt/app

RUN pip install pipenv
RUN pipenv lock
RUN pipenv sync

EXPOSE 8080/tcp

CMD ["pipenv", "run", "start"]
