FROM python:3.11-slim AS builder

COPY requirements.txt requirements.txt
COPY requirements_test.txt requirements_test.txt

RUN pip install --upgrade pip && pip install --user --no-cache-dir -r requirements.txt

ARG ENV
RUN if [ "$ENV" = "test" ]; then \
    pip install --user --no-cache-dir -r requirements_test.txt; \
    fi;

FROM python:3.11-slim AS production

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

COPY --from=builder /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

WORKDIR /shopAPI

COPY . /shopAPI/
