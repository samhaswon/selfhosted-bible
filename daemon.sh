#!/usr/bin/env bash

if [ -n "$API_KEY" ]; then
  echo -n "$API_KEY" > '/usr/src/app/api-key.txt'
fi

exec waitress-serve --port=5000 --call "main:create_app"
