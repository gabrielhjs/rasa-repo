FROM rasa/rasa:3.1.0-spacy-en

SHELL ["/bin/bash", "-c"]

ENV LANG C.UTF-8

WORKDIR /app

COPY ./endpoints.yml ./endpoints.yml
COPY ./credentials.yml ./credentials.yml
COPY ./domain.yml ./domain.yml
COPY ./models ./models
COPY ./addons ./addons

USER root

RUN python -m spacy download pt_core_news_md

USER 1001

RUN rasa telemetry disable

EXPOSE 5005

CMD ["run", "-m", "./models", "--enable-api", "--debug"]
