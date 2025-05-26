#!/usr/bin/env ash

# Retrieve any missing Bibles
test -f /usr/src/app/bibles/json-bibles/acv.json.pbz2 || wget -O /usr/src/app/bibles/json-bibles/acv.json.pbz2 https://github.com/samhaswon/selfhosted-bible/raw/main/bibles/json-bibles/acv.json.pbz2
test -f /usr/src/app/bibles/json-bibles/akjv.json.pbz2 || wget -O /usr/src/app/bibles/json-bibles/akjv.json.pbz2 https://github.com/samhaswon/selfhosted-bible/raw/main/bibles/json-bibles/akjv.json.pbz2
test -f /usr/src/app/bibles/json-bibles/asv.json.pbz2 || wget -O /usr/src/app/bibles/json-bibles/asv.json.pbz2 https://github.com/samhaswon/selfhosted-bible/raw/main/bibles/json-bibles/asv.json.pbz2
test -f /usr/src/app/bibles/json-bibles/bbe.json.pbz2 || wget -O /usr/src/app/bibles/json-bibles/bbe.json.pbz2 https://github.com/samhaswon/selfhosted-bible/raw/main/bibles/json-bibles/bbe.json.pbz2
test -f /usr/src/app/bibles/json-bibles/bsb.json.pbz2 || wget -O /usr/src/app/bibles/json-bibles/bsb.json.pbz2 https://github.com/samhaswon/selfhosted-bible/raw/main/bibles/json-bibles/bsb.json.pbz2
test -f /usr/src/app/bibles/json-bibles/darby.json.pbz2 || wget -O /usr/src/app/bibles/json-bibles/darby.json.pbz2 https://github.com/samhaswon/selfhosted-bible/raw/main/bibles/json-bibles/darby.json.pbz2
test -f /usr/src/app/bibles/json-bibles/dra.json.pbz2 || wget -O /usr/src/app/bibles/json-bibles/dra.json.pbz2 https://github.com/samhaswon/selfhosted-bible/raw/main/bibles/json-bibles/dra.json.pbz2
test -f /usr/src/app/bibles/json-bibles/ebr.json.pbz2 || wget -O /usr/src/app/bibles/json-bibles/ebr.json.pbz2 https://github.com/samhaswon/selfhosted-bible/raw/main/bibles/json-bibles/ebr.json.pbz2
test -f /usr/src/app/bibles/json-bibles/gnv.json.pbz2 || wget -O /usr/src/app/bibles/json-bibles/gnv.json.pbz2 https://github.com/samhaswon/selfhosted-bible/raw/main/bibles/json-bibles/gnv.json.pbz2
test -f /usr/src/app/bibles/json-bibles/kjv.json.pbz2 || wget -O /usr/src/app/bibles/json-bibles/kjv.json.pbz2 https://github.com/samhaswon/selfhosted-bible/raw/main/bibles/json-bibles/kjv.json.pbz2
test -f /usr/src/app/bibles/json-bibles/kjv1611.json.pbz2 || wget -O /usr/src/app/bibles/json-bibles/kjv1611.json.pbz2 https://github.com/samhaswon/selfhosted-bible/raw/main/bibles/json-bibles/kjv1611.json.pbz2
test -f /usr/src/app/bibles/json-bibles/lsv.json.pbz2 || wget -O /usr/src/app/bibles/json-bibles/lsv.json.pbz2 https://github.com/samhaswon/selfhosted-bible/raw/main/bibles/json-bibles/lsv.json.pbz2
test -f /usr/src/app/bibles/json-bibles/rnkjv.json.pbz2 || wget -O /usr/src/app/bibles/json-bibles/rnkjv.json.pbz2 https://github.com/samhaswon/selfhosted-bible/raw/main/bibles/json-bibles/rnkjv.json.pbz2
test -f /usr/src/app/bibles/json-bibles/rv2004.json.pbz2 || wget -O /usr/src/app/bibles/json-bibles/rv2004.json.pbz2 https://github.com/samhaswon/selfhosted-bible/raw/main/bibles/json-bibles/rv2004.json.pbz2
test -f /usr/src/app/bibles/json-bibles/rwv.json.pbz2 || wget -O /usr/src/app/bibles/json-bibles/rwv.json.pbz2 https://github.com/samhaswon/selfhosted-bible/raw/main/bibles/json-bibles/rwv.json.pbz2
test -f /usr/src/app/bibles/json-bibles/ukjv.json.pbz2 || wget -O /usr/src/app/bibles/json-bibles/ukjv.json.pbz2 https://github.com/samhaswon/selfhosted-bible/raw/main/bibles/json-bibles/ukjv.json.pbz2
test -f /usr/src/app/bibles/json-bibles/web.json.pbz2 || wget -O /usr/src/app/bibles/json-bibles/web.json.pbz2 https://github.com/samhaswon/selfhosted-bible/raw/main/bibles/json-bibles/web.json.pbz2
test -f /usr/src/app/bibles/json-bibles/ylt.json.pbz2 || wget -O /usr/src/app/bibles/json-bibles/ylt.json.pbz2 https://github.com/samhaswon/selfhosted-bible/raw/main/bibles/json-bibles/ylt.json.pbz2

[[ -z "${ESV_API_KEY}" || -z "${DOCKER_STARTED}" ]] && echo -n "$ESV_API_KEY" > '/usr/src/app/esv-api-key.txt' || echo -n "" > '/usr/src/app/esv-api-key.txt'
export DOCKER_STARTED="true"

set -e
exec waitress-serve --port=5000 --call "main:create_app"
