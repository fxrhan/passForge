#!/bin/bash
# Cross-platform verification script for Linux/macOS
# Run this on Linux/macOS to verify compatibility

echo "=================================="
echo "Cross-Platform Verification Script"
echo "Platform: $(uname -s)"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
echo ""

# Run compatibility tests
echo "Running compatibility tests..."
python3 test_compatibility.py
echo ""

# Test basic commands
echo "Testing basic commands..."
echo "1. Version check:"
python3 longtongue.py -v
echo ""

echo "2. Help display:"
python3 longtongue.py -h
echo ""

echo "=================================="
echo "Verification complete!"
echo "=================================="
