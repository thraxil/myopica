# Django settings for myopica project.
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Anders Pearson', 'anders@columbia.edu'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myopica',
        'HOST': '',
        'PORT': 5432,
        'USER': '',
        'PASSWORD': '',
        }
}

if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            'HOST': '',
            'PORT': '',
            'USER': '',
            'PASSWORD': '', }}

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1
USE_I18N = False

MEDIA_ROOT = '/var/tmp/myopica/media/'
MEDIA_URL = '/uploads/'
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = 'daod0^($fi6%pcy8(ihsj8$e0!&4@+=s8())redma#z9)v9d8*'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
     'django.contrib.auth.context_processors.auth',
     'django.core.context_processors.debug',
     'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django_statsd.middleware.GraphiteRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'myopica.urls'

TEMPLATE_DIRS = (
    "/home/anders/code/python/myopica/portfolio/templates/"
)

INSTALLED_APPS = (
    'myopica.portfolio',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.markup',
    'south',
    'django_nose',
    'django.contrib.sitemaps',
    'django_statsd',
    'gunicorn',
)

THUMBNAIL_SUBDIR = "thumbs"
SOUTH_TESTS_MIGRATE = False
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=myopica',
]

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = True

STATSD_CLIENT = 'statsd.client'
STATSD_PREFIX = 'myopica'
STATSD_HOST = '127.0.0.1'
STATSD_PORT = 8125
STATSD_PATCHES = ['django_statsd.patches.db', ]
