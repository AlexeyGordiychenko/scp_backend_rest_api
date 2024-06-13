FROM python:3.11-slim AS builder

COPY requirements.txt requirements.txt
COPY requirements_test.txt requirements_test.txt

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

ARG ENV
RUN if [ "$ENV" = "test" ]; then \
    pip install --no-cache-dir -r requirements_test.txt; \
    fi;

FROM python:3.11-slim AS production

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

COPY --from=builder /usr/local /usr/local

ENV PATH=/usr/local/bin:$PATH

RUN useradd -m appuser
USER appuser

WORKDIR /shopAPI

COPY . /shopAPI/

RUN if [ "$ENV" = "test" ]; then \
    mkdir -p /shopAPI/htmlcov; \
    chown -R appuser:appuser /shopAPI/htmlcov; \
    chmod 755 /shopAPI/htmlcov; \
    fi;