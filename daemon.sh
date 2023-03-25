#!/usr/bin/env ash

if [ -n "$API_KEY" ]
then
  echo -n "$API_KEY" > '/usr/src/app/esv-api-key.txt'
else
  echo -n "" > '/usr/src/app/esv-api-key.txt'
fi

set -e

exec waitress-serve --port=5000 --call "main:create_app"
