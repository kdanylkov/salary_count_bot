FROM python:3.10

EXPOSE 8081/tcp

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /bot

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt

RUN chmod 755 .

COPY . .


