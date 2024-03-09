FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# For now this project doesn't rely on any third party packages
# RUN pip install --no-cache-dir -r requirements.txt

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Define environment variable
ENV USE_DB 0

CMD ["python", "-u", "./src/server.py"]
