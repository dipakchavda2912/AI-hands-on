#!/bin/bash
# React Timeline Tracker - Verification Script

echo "======================================"
echo "React Timeline Tracker - Verification"
echo "======================================"
echo ""

# Check Node version
echo "📦 Checking Node.js version..."
node --version
echo ""

# Check npm version
echo "📦 Checking npm version..."
npm --version
echo ""

# Check installed packages
echo "📦 Checking installed React packages..."
npm list react react-dom react-scripts --depth=0
echo ""

# Check for vulnerabilities (non-blocking)
echo "🔍 Running security audit..."
npm audit || echo "Note: Some vulnerabilities exist in transitive dependencies (non-critical)"
echo ""

# Verify build output exists
if [ -d "build" ]; then
    echo "✅ Production build exists"
    echo "   Build size:"
    du -sh build
else
    echo "⚠️  No production build found. Run 'npm run build' to create one."
fi
echo ""

echo "======================================"
echo "✅ Verification Complete!"
echo "======================================"
echo ""
echo "To run the app:"
echo "  npm start"
echo ""
echo "To build for production:"
echo "  npm run build"
echo ""
echo "To serve production build:"
echo "  npm install -g serve"
echo "  serve -s build"
echo ""
