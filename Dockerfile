FROM python:3.12-slim

ARG VERSION=dev
ARG BUILD_DATE=unknown

WORKDIR /app

LABEL org.opencontainers.image.title="starter-app"
LABEL org.opencontainers.image.description="Capstone calculator API for CI/CD demos"
LABEL org.opencontainers.image.version=$VERSION
LABEL org.opencontainers.image.created=$BUILD_DATE

COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY src ./src

EXPOSE 8000

ENV APP_NAME=starter-app
ENV APP_VERSION=$VERSION
ENV APP_ENV=container
ENV HOST=0.0.0.0
ENV PORT=8000

CMD ["python", "-m", "src.app"]