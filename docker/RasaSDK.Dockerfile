FROM rasa/rasa-sdk:3.1.0

WORKDIR /app

COPY ./actions ./actions

EXPOSE 5055