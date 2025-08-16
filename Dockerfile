# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for security tools
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    nmap \
    nikto \
    hydra \
    sqlmap \
    dnsutils \
    net-tools \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements_enhanced.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_enhanced.txt

# Copy all penetration testing scripts and tools
COPY *.py ./
COPY tools/ ./tools/

# Copy README and other documentation
COPY README.md ./

# Create directories for results and reports
RUN mkdir -p /app/results /app/logs /app/reports

# Set environment variables
ENV PYTHONPATH=/app
ENV PENTEST_OUTPUT_DIR=/app/results

# Create a non-root user for security
RUN useradd -m -u 1000 pentester && \
    chown -R pentester:pentester /app
USER pentester

# Expose port for any web interfaces (if needed)
EXPOSE 8080

# Default command - run the enhanced pentest automation
CMD ["python", "enhanced_pentest_automation.py"]
