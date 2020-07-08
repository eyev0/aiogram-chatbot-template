FROM python:3.8-slim-buster as build
LABEL description="Telegram Bot"

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/"
ENV PATH "/usr/src/scripts:${PATH}"

WORKDIR /usr/src/

COPY ./requirements.txt /usr/src/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/
RUN pip install --no-cache-dir -e .

RUN chmod +x scripts/* && \
    pybabel compile -d locales -D bot

STOPSIGNAL SIGINT
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["run-polling"]
