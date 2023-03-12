# syntax=docker/dockerfile:1
FROM debian:bullseye-slim

# Setup app
WORKDIR /usr/src/app
COPY --chmod=0755 . .

# Setup debian
RUN apt update; \
	apt install -y --no-install-recommends --no-install-suggests \
		python3-pip && \
      pip install --no-cache-dir setuptools && \
      python3 setup.py bdist_wheel && \
      pip install --no-cache-dir -e . && \
      pip uninstall setuptools -y && \
      rm -rf /usr/lib/python3/dist-packages/ && \
    apt remove python3-pip python-pip-whl python3-distutils python3-lib2to3 python3-wheel \
        ca-certificates python3-pkg-resources -y; \
    apt auto-clean -y && \
    rm requirements.txt && \
    rm -rf build/ dist/ esv_web.egg-info/ && \
    rm -rf /usr/share/doc/ && \
    rm -rf /usr/lib/python3.9/pydoc_data && \
    rm -rf /usr/lib/python3.9/test && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 5000

CMD [ "/usr/src/app/daemon.sh" ]