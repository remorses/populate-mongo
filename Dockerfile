FROM python:3.7.4-alpine

ENV PYTHONUNBUFFERED=1
WORKDIR /

COPY requirements.txt /

RUN pip install -r requirements.txt

COPY src /src/

RUN cd /

CMD ["python", "-m", "src", "/conf.yml"]

