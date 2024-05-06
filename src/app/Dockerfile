FROM python:3.11-slim AS builder

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim AS production

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

COPY --from=builder /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

WORKDIR /app

COPY . /app
