FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Define environment variable used for selecting which server to run inside the container, one with a db or one with an in-memory data structure.
ENV USE_DB 0

CMD ["python", "-u", "./src/server.py"]
