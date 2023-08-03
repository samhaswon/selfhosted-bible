# syntax=docker/dockerfile:1

FROM python:3-alpine as build-stage

RUN mkdir /svc
WORKDIR /svc
COPY requirements.txt /svc

# Install required apk packages
RUN echo "***** Getting required packages *****" && \
    apk add --no-cache --update  \
    gcc \
    musl-dev \
    linux-headers && \
    pip install --upgrade pip

# Build dependencies
RUN echo "***** Building dependencies *****" && \
    pip wheel -r /svc/requirements.txt --wheel-dir=/svc/wheels

FROM python:3-alpine as application

ENV PYTHONUNBUFFERED=TRUE

# Get build-stage files
COPY --from=build-stage /svc /usr/src/app
WORKDIR /usr/src/app
RUN echo "***** Installing dependencies *****" && \
    pip install --no-index --find-links=/usr/src/app/wheels -r requirements.txt

# Setup app
COPY --chmod=0755 . .

EXPOSE 5000

STOPSIGNAL SIGKILL
CMD [ "/usr/src/app/daemon.sh" ]
VOLUME /usr/src/app/bibles/json-bibles
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD wget http://localhost:5000/health -q -O - > /dev/null 2>&1
