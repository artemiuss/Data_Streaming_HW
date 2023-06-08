FROM python:3-slim-bullseye
LABEL stage=builder
WORKDIR /app
COPY requirements.txt ./ 
RUN pip install --root-user-action=ignore --no-cache-dir --user -r requirements.txt

FROM python:3-slim-bullseye
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY *.py ./ 
#EXPOSE 8080 8081 8082
ENTRYPOINT ["python"]
CMD [""]
