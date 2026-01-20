#!/bin/bash
# Minimal test runner script for Pink Morsel Dashboard
# This script runs the simple_test.py file

echo "========================================"
echo "Running Pink Morsel Dashboard Tests"
echo "========================================"

# Run the Python test script
python simple_test.py

# Capture the exit code
TEST_EXIT_CODE=$?

echo "========================================"

# Return the appropriate exit code
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✅ All tests passed!"
    exit 0
else
    echo "❌ Tests failed"
    exit 1
fi