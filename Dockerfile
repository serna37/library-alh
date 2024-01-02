FROM python:3.11.4-slim-bullseye

WORKDIR /asset

COPY ./app /asset/app

RUN python -m pip install -U pip \
    && python -m pip install -r requirements.txt \
    && touch app/data.db \
    && chmod 777 app/data.db

CMD ["python", "server.py"]
