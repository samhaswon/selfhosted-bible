# syntax=docker/dockerfile:1
FROM python:3-slim

WORKDIR /usr/src/app
COPY . .

# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir setuptools && \
    python3 setup.py bdist_wheel && \
    pip install --no-cache-dir -e . && \
    pip uninstall setuptools -y && \
    rm requirements.txt && \
    rm -rf build/ dist/ esv_web.egg-info/

RUN echo "" > api-key.txt

EXPOSE 5000

CMD [ "/usr/src/app/daemon.sh" ]