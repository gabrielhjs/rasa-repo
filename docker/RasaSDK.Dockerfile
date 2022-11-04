FROM rasa/rasa-sdk:3.2.1

WORKDIR /app

COPY ./actions ./actions
COPY ./sdk.requirements.txt ./requirements.txt
COPY ./messages.json ./messages.json

USER root

RUN pip install -r requirements.txt

USER 1001

EXPOSE 5055