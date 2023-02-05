# Use a Python base image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Change the working directory to /app/api_code
WORKDIR /app/delivery_fee_api/api_code

# Run the API server, tests and client in parallel using the "&" symbol and "wait" command
CMD ["/bin/bash", "-c", "python delivery_fee_api.py & python tests.py && wait"]
