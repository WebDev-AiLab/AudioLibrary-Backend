FROM python:3.10.5
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update \
    && apt-get install -y postgresql postgresql-contrib
RUN apt-get install -y libmagic-dev
COPY . .
RUN apt-get update -y
RUN apt-get install python3-magic
RUN pip install --upgrade pip
RUN pip install python-magic
RUN pip install -r requirements.txt


