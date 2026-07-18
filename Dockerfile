FROM python:3.11-slim

WORKDIR /app

# Install system dependencies needed by sentence-transformers / faiss
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py agent.py ./

# Streamlit config — disable telemetry, set port
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_HEADLESS=true

EXPOSE 8080

CMD ["streamlit", "run", "app.py"]
