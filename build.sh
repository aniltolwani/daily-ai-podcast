#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting build process..."

# Install package and dependencies
echo "📦 Installing package and dependencies..."
pip install -e .
pip install 'playwright>=1.35.0'

# Install Playwright and its dependencies using system package manager
echo "🎭 Setting up Playwright..."
apt-get update && apt-get install -y \
    libc6 \
    libstdc++6 \
    chromium \
    chromium-driver

# Set environment variable to use system Chrome
export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
export PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium

# Verify installation
echo "✅ Verifying installation..."
python -m daily_ai_podcast.main --version || echo "⚠️  Version check failed, but continuing..."

echo "🎉 Build complete!"