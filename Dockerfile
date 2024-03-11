FROM python:3.8-slim

WORKDIR /usr/src

COPY . .

EXPOSE 3000

ENV USE_DB 0

CMD ["python", "-u", "./src/server.py"]
