# Use Python base image
FROM python:3.11.4-slim

# Copy requirements.txt to the container
COPY requirements.txt /tmp/

# Install dependencies
RUN apt-get update && apt-get install -y git curl
RUN pip3 install --upgrade pip && pip3 install -r /tmp/requirements.txt

# Copy the Python backend code into the container
COPY . .

# Build the React app
# You can replace "npm" with "yarn" if you prefer using Yarn
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs
    # apt-get install -y nodejs && \
#     npm cache clear --force && \ 
#     npm install && \
#     npm run build

# # Expose the port that the backend will run on
# EXPOSE 8000

# Start the FastAPI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
