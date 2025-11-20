#!/bin/bash
#
# Test Runner Script for TelcoX Backend
#
# Uses Django's test runner with SQLite test database
#
# Usage:
#   ./run_tests.sh                          # Run all tests
#   ./run_tests.sh apps.customers           # Run specific app
#   ./run_tests.sh apps.customers.tests.test_models  # Run specific module
#   ./run_tests.sh apps.customers.tests.test_models.CustomerModelTestCase  # Run specific class
#

# Unset any existing Django settings env var
unset DJANGO_SETTINGS_MODULE

# Run Django tests with test_settings
DJANGO_SETTINGS_MODULE=config.test_settings python manage.py test "$@"
