"""
pytest configuration for TelcoX backend tests.

This file provides pytest fixtures and configuration for running tests.
Forces test_settings to be used even if DJANGO_SETTINGS_MODULE env var is set.
"""
import os
import sys
import pytest
import django
from django.conf import settings


# Force test settings BEFORE any Django initialization
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.test_settings'


def pytest_configure(config):
    """
    Configure pytest to force use of test settings.
    
    This runs before tests and ensures SQLite is used regardless of
    environment variables set in docker-compose.yml.
    """
    # Force test settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.test_settings')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.test_settings'
    
    # If Django is already configured, this is a no-op
    # If not, this will configure it with test_settings
    if not settings.configured:
        django.setup()


@pytest.fixture(scope='session')
def django_db_setup():
    """
    Override default django_db_setup to ensure proper database configuration.
    Uses SQLite in-memory database for faster tests.
    """
    from django.conf import settings
    
    # Verify we're using SQLite
    db_engine = settings.DATABASES['default']['ENGINE']
    if db_engine != 'django.db.backends.sqlite3':
        print(f"\n⚠️  WARNING: Expected SQLite but got {db_engine}")
        print("Make sure to run tests with: ./run_tests.sh or unset DJANGO_SETTINGS_MODULE\n")
    
    # Let pytest-django handle the rest (migrations, etc.)
    pass


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Automatically enable database access for all tests.
    This removes the need to mark tests with @pytest.mark.django_db
    """
    pass
