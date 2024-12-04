# Use a lightweight Python base image
FROM python:3.10-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create and set the working directory
WORKDIR /app

# Install necessary build tools for Python dependencies
#RUN apt-get update && apt-get install -y --no-install-recommends \
#    gcc libffi-dev && \
#    apt-get clean && \
#    rm -rf /var/lib/apt/lists/*

# Copy only the requirements first to optimize Docker cache
COPY requirements.txt /app/requirements.txt

## Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    pip install Flask-Mail==0.10.0 && \
    pip install colorlog==0.1 && \
    pip install python-dotenv

# Add a non-root user for improved security
RUN useradd -m appuser && \
    chown -R appuser /app

# Copy the rest of the application code
COPY . /app

# Switch to the non-root user
USER appuser

# Expose the port your app will run on
EXPOSE 5000

# Define the default command to run the app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
