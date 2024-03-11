FROM python:3.8-slim

WORKDIR /usr/src

COPY . .

EXPOSE 3000

ENV USE_DB 0

CMD if [ "$USE_DB" = "1" ]; then \
        exec python -u ./src/server_with_db.py; \
    else \
        exec python -u ./src/server.py; \
    fi
