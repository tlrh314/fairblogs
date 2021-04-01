FROM python:3.9-slim-buster
ENV PYTHONUNBUFFERED 1

LABEL maintainer="Timo Halbesma <timo@projectcece.nl>"

WORKDIR /fairblogs

# Install system dependencies.
RUN set -ex && \
    apt-get update && \
\
    # Install Runtime dependencies ...
    apt-get install -y --no-install-recommends \
        # ... a compiler (build)
        build-essential gcc \
        # ... for a proper editor
        vim \
        # ... for the healthcheck
        curl \
        # ... for monitoring
        htop \
        # ... for internal routing of uWSGI
        libpcre3 libpcre3-dev \
        # ... for communication with the database
        mariadb-client libmariadb-dev-compat\
        # ... for Pillow
        python3-dev python3-setuptools libtiff5-dev libjpeg-dev zlib1g-dev \
        libfreetype6-dev liblcms2-dev libwebp-dev libharfbuzz-dev libfribidi-dev \
        tcl8.6-dev tk8.6-dev python3-tk \
        # ... to sync clocks
        ntp && \
\
    # Create runtime user (because uWSGI prefers non-root)
    groupadd -g 1000 fairblogs && \
    useradd -r -u 1000 -g fairblogs fairblogs -s /bin/bash -d /fairblogs && \
\
    # Cleanup
    rm -rf /var/lib/apt/lists/*

# Install our application requirements
COPY requirements.txt /fairblogs/requirements.txt
RUN set -ex && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /fairblogs/requirements.txt && \
    pip install uwsgi mysqlclient && \
    chown -R fairblogs:fairblogs /fairblogs

COPY . /fairblogs
RUN chown -R fairblogs:fairblogs /fairblogs

USER fairblogs

ENTRYPOINT ["/fairblogs/entrypoint.sh"]
