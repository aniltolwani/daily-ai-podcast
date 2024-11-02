FROM mcr.microsoft.com/playwright/python:v1.48.0-jammy

WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY src/ ./src/

# Install the package and its dependencies
RUN pip install -e . && \
    playwright install chromium && \
    playwright install-deps

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

# Command to run the application
CMD ["python", "-m", "daily_ai_podcast.main"]