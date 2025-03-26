# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.10-alpine

EXPOSE 8002

WORKDIR /app

COPY requirements.txt /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . /app

RUN opentelemetry-bootstrap -a install
ENTRYPOINT ["opentelemetry-instrument"]
CMD ["fastapi", "run", "app.py", "--host", "0.0.0.0", "--port", "8000"]
