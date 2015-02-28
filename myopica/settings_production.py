# flake8: noqa
from settings_shared import *
import os.path

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

STATIC_ROOT = os.path.join(os.path.dirname(__file__), "../media")
STATICFILES_DIRS = ()
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

if 'migrate' not in sys.argv:
    INSTALLED_APPS = INSTALLED_APPS + [
        'raven.contrib.django.raven_compat',
    ]


# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass
