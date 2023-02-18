# syntax=docker/dockerfile:1
FROM python:3-slim

WORKDIR /usr/src/app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Build the program and install
RUN python3 setup.py bdist_wheel
RUN pip install -e .

RUN echo "" > api-key.txt

EXPOSE 5000

CMD [ "/usr/src/app/daemon.sh" ]