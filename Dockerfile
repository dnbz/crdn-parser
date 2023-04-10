FROM python:3.11-slim

WORKDIR /app

# install pdm and supervisor
RUN pip install -U pip setuptools wheel
RUN pip install pdm supervisor

COPY pyproject.toml pdm.lock ./
RUN pdm install --prod --no-lock --no-editable

COPY ./docker/supervisord.conf /etc/supervisord.conf
COPY ./docker/supervisord.conf.d /etc/supervisor/conf.d

COPY . .

ENTRYPOINT ["./entrypoint.sh"]
