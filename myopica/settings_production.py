# flake8: noqa
from settings_shared import *

TEMPLATE_DIRS = (
    "/var/www/myopica/myopica/myopica/templates",
)
MEDIA_ROOT = '/var/www/myopica/media/'
DEBUG = False
TEMPLATE_DEBUG = DEBUG

STATICFILES_DIRS = ()
STATIC_ROOT = "/var/www/myopica/myopica/media/"

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass
