"""
Django test settings for TelcoX.

This file extends the main settings and overrides database configuration
to use SQLite for testing, which is:
- Faster than MySQL
- Doesn't require database creation permissions
- Runs entirely in memory
- Standard practice for Django unit tests
"""
from .settings import *  # noqa


# Override database to use SQLite for tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'ATOMIC_REQUESTS': True,
    }
}

# Disable migrations for faster test runs (pytest-django does this with --nomigrations)
# But we can also do it here as a fallback
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


# Uncomment this line if you want to disable migrations entirely for tests
# MIGRATION_MODULES = DisableMigrations()

# Speed up password hashing in tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable debug toolbar if it's installed
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: False,
}

# Use faster JSON serializer for tests and disable pagination
REST_FRAMEWORK = {
    **REST_FRAMEWORK,  # Keep existing REST_FRAMEWORK settings
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': None,  # Disable pagination for tests
}
