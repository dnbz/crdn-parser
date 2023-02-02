FROM python:alpine3.16 as base

WORKDIR /app

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN apk add --no-cache \
        g++ gcc \
        py3-pybind11-dev \
    && pip install poetry

COPY ./poetry.lock ./pyproject.toml ./poetry.toml ./
RUN poetry install

FROM base as final

RUN apk add --no-cache \
        fish \
        tzdata \
        curl \
        supervisor \
        busybox-initscripts openrc \
        ca-certificates \
        poetry \
        libpq


COPY --from=builder /root/.cache/pypoetry /root/.cache/pypoetry
COPY ./docker/supervisord.conf /etc/supervisord.conf

# COPY ./ ./

COPY ./entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
