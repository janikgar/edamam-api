FROM python:3.9.6

RUN mkdir -p /project/edamam_flask && \
    useradd -u 1000 -d /project user && \
    chown user. /project
COPY edamam_flask/** /project/edamam_flask
COPY setup.py /project

WORKDIR /project
RUN pip install -r edamam_flask/prod-requirements.txt && \
    pip install -e .
USER 1000
EXPOSE 8000

ENTRYPOINT [ "gunicorn", "-w 1", "--worker-class=gevent", "--bind=0.0.0.0", "edamam_flask.app:create_app()" ]