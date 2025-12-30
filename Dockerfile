# Use the official Python image
FROM python:3.13.0-alpine3.20

# Working directory inside the container
WORKDIR /app

# Copy the Python script into the container
COPY sum.py /app/sum.py

# Keep container running (useful later for Jenkins docker exec)
CMD ["tail", "-f", "/dev/null"]
