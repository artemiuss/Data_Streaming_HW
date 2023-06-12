FROM python:3 AS builder
LABEL stage=builder
WORKDIR /app
COPY requirements.txt ./
RUN pip install --root-user-action=ignore --no-cache-dir --user -r requirements.txt
RUN sed -i~ '/^KAFKA_HOST=/s/=.*/="kafka1"/' .env

FROM python:3
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY *.py ./
ENTRYPOINT ["python"]
CMD [""]
