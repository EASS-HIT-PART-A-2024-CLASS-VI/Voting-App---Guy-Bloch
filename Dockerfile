# Backend Dockerfile
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy dependencies
COPY app/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ .

# Expose backend port
EXPOSE 8000

# Run backend server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
