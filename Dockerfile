FROM python:3 AS builder
LABEL stage=builder
WORKDIR /app
COPY requirements.txt .env ./
RUN pip install --root-user-action=ignore --no-cache-dir --user -r requirements.txt
RUN sed -i '/^KAFKA_HOST=/s/=.*/="172.17.0.1"/' .env
RUN sed -i '/^KAFKA_PORT=/s/=.*/="9092"/' .env

FROM python:3
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app/.env /app/.env
COPY *.py ./
COPY *.sql ./
ENTRYPOINT ["python"]
CMD [""]
