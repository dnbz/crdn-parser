#!/bin/sh

echo "Starting the parser..."

if [ -f /runtime/app/requirements.txt ];then
    pip install -r /runtime/app/requirements.txt
fi

if [ -f /runtime/app/pyproject.toml ];then
    poetry install --only main
fi


if [ "$STOP_PARSER" ];then
    echo "Parser is disabled through an environment variable. Idling..."
    sleep
fi

crontab /etc/mycrontab
crond

exec supervisord
