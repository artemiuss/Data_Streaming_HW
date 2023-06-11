FROM python:3-slim-bullseye AS builder
LABEL stage=builder
WORKDIR /app
COPY requirements.txt ./
RUN pip install --root-user-action=ignore --no-cache-dir --user -r requirements.txt

FROM python:3-slim-bullseye
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY *.py ./
ENTRYPOINT ["python"]
CMD [""]
