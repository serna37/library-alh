FROM python:3.11.4-slim-bullseye

WORKDIR /asset/app

COPY ./app /asset/app

RUN python -m pip install -U pip \
    && python -m pip install -r requirements.txt \
    && touch data.db \
    && chmod 777 data.db

CMD ["python", "server.py"]
