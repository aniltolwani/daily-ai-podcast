#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting build process..."

# Install package and dependencies
echo "📦 Installing package and dependencies..."
pip install -e .
pip install 'playwright>=1.35.0'

# Install Playwright and its dependencies
echo "🎭 Setting up Playwright..."
playwright install chromium
playwright install-deps

# Verify installation
echo "✅ Verifying installation..."
python -m daily_ai_podcast.main --version || echo "⚠️  Version check failed, but continuing..."

echo "🎉 Build complete!"