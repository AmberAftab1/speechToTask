FROM python:3.7

RUN apt-get update && apt-get -y install gcc

WORKDIR /app

ENV PYTHONBUFFERED 1


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 8000
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

