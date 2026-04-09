FROM python:3.12-slim

RUN apt-get update && \
    apt-get install --yes --no-install-recommends build-essential curl && \
    pip install --no-cache-dir uv && \
    apt-get purge -y build-essential && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

# Default container profile: repository-root install with committed reproducibility inputs.
# This image demonstrates the published dependency model using the SQLite + Uvicorn profile.
RUN uv pip install --system \
    -c constraints/base.txt \
    -c constraints/runner-uvicorn.txt \
    ".[sqlite,uvicorn]"

EXPOSE 8000

ENV \
    TIGRBL_AUTH_INSTALL_PROFILE="sqlite+uvicorn" \
    PG_HOST="" \
    PG_PORT="5432" \
    PG_DB="" \
    PG_USER="" \
    PG_PASS="" \
    REDIS_HOST="" \
    REDIS_PASSWORD=""

CMD ["python", "-m", "uvicorn", "tigrbl_auth.app:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info", "--proxy-headers"]
