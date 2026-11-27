FROM internetsystemsconsortium/bind9@sha256:978201d91548ec63c3b1c1befd5e6a3c9fa127f79f9058fd82d8e3493fe90ce1

RUN apk add --no-cache krb5 krb5-server py3-idna python3 uv \
    && apk add --no-cache --virtual .gss-build build-base krb5-dev python3-dev \
    && uv venv --no-managed-python --python /usr/bin/python3 --system-site-packages /opt/dns-peer \
    && uv pip install --no-cache --python /opt/dns-peer/bin/python 'gssapi==1.12.0' 'decorator==5.3.1' \
    && apk del .gss-build

COPY run.sh probe.py /opt/dns-interop/
ENTRYPOINT ["/bin/sh", "/opt/dns-interop/run.sh"]
