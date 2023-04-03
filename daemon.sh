#!/usr/bin/env ash

[[ -z "${ESV_API_KEY}" || -z "${DOCKER_STARTED}" ]] && echo -n "$ESV_API_KEY" > '/usr/src/app/esv-api-key.txt' || echo -n "" > '/usr/src/app/esv-api-key.txt'
export DOCKER_STARTED="true"

set -e
exec waitress-serve --port=5000 --call "main:create_app"
