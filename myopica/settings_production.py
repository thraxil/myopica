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

AWS_STORAGE_BUCKET_NAME = "thraxil-myopica-static-prod"
AWS_PRELOAD_METADATA = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'cacheds3storage.CompressorS3BotoStorage'
CLOUDFRONT_DOMAIN = "d3bk6m0iptukrc.cloudfront.net"
S3_URL = 'https://%s/' % CLOUDFRONT_DOMAIN
STATIC_URL = 'https://%s/media/' % CLOUDFRONT_DOMAIN
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_URL = STATIC_URL
DEFAULT_FILE_STORAGE = 'cacheds3storage.MediaRootS3BotoStorage'
MEDIA_URL = S3_URL + '/media/'
COMPRESS_STORAGE = 'cacheds3storage.CompressorS3BotoStorage'
AWS_QUERYSTRING_AUTH = False


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
