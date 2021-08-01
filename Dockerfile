FROM python:3.9.6

RUN mkdir -p /project/api && \
    useradd -u 1000 -d /project user && \
    chown user. /project
COPY api/** /project/api

WORKDIR /project/api
RUN pip install -r prod-requirements.txt

USER 1000
EXPOSE 8000

ENTRYPOINT [ "gunicorn", "-w 4", "--worker-class=gevent", "app:app" ]