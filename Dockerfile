# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy app code & data
COPY . .

# Expose ports (Cloud Run uses $PORT, default 8080; locally 5002)
EXPOSE 8080
EXPOSE 5002

# Launch Flask
CMD ["python", "server.py"]