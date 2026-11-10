# Use a lightweight Linux base image with Python 3.12
FROM python:3.12-slim

# Install C++ compiler (g++) and cleanup package cache
RUN apt-get update && apt-get install -y --no-install-recommends \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /sandbox

# Default command
CMD ["bash"]
