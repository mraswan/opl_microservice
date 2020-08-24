FROM alpine:3.1
#FROM python:2.7-slim

# Update
RUN apk add --update gcc g++ python python-dev py-pip
COPY requirements.txt /requirements.txt

# Install app dependencies
RUN pip install -r /requirements.txt

# Bundle app source
COPY gunicorn.conf /gunicorn.conf
COPY logging.conf /logging.conf
COPY wsgi.py /run.py
COPY __init__.py /__init__.py
COPY RfyWAtsonDiscovery /RfyWAtsonDiscovery
COPY config /config
COPY instance /instance


EXPOSE  5000
#CMD ["gunicorn", "--bind 0.0.0.0:5000 run:rfyAPIApp"]
ENTRYPOINT ["gunicorn", "--config", "/gunicorn.conf", "--log-config", "/logging.conf", "-b", ":5000", "run:rfyAPIApp"]