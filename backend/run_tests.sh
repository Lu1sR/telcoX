#!/bin/bash
#
# Test Runner Script for TelcoX Backend
#
# Uses Django's test runner with SQLite test database
#
# Usage:
#   ./run_tests.sh                          # Run all tests
#   ./run_tests.sh --cov                    # Run with coverage report
#   ./run_tests.sh --cov-html               # Run with HTML coverage report
#   ./run_tests.sh apps.customers           # Run specific app
#   ./run_tests.sh apps.customers.tests.test_models  # Run specific module
#

# Unset any existing Django settings env var
unset DJANGO_SETTINGS_MODULE

# Check if coverage flag is present
if [ "$1" = "--cov" ]; then
    shift  # Remove --cov from arguments
    echo "Running tests with coverage..."
    DJANGO_SETTINGS_MODULE=config.test_settings coverage run --source='apps' manage.py test "$@"
    echo ""
    echo "Coverage Report:"
    coverage report
    
elif [ "$1" = "--cov-html" ]; then
    shift  # Remove --cov-html from arguments
    echo "Running tests with HTML coverage..."
    DJANGO_SETTINGS_MODULE=config.test_settings coverage run --source='apps' manage.py test "$@"
    coverage html
    echo ""
    echo "Coverage Report:"
    coverage report
    echo ""
    echo "HTML report generated at: htmlcov/index.html"
    
else
    # Run Django tests with test_settings (no coverage)
    DJANGO_SETTINGS_MODULE=config.test_settings python manage.py test "$@"
fi
