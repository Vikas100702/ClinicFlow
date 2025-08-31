# 1. Lightweight Python base image
FROM python:3.11-slim

# 2. Set working directory inside the container
WORKDIR /app

# 3. Only copy requirements first for caching benefits
COPY requirements.txt .

# 4. Install dependencies and clean pip cache for smaller image size
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

# 5. Copy the FastAPI application code
COPY app ./app


COPY .env .env

WORKDIR /app/app
# 6. Expose the port your app will run on
EXPOSE 8000

# 7. Run the FastAPI application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
