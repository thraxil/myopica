# Django settings for myopica project.
import os.path
from thraxilsettings.shared import common

app = 'myopica'
base = os.path.dirname(__file__)

locals().update(common(app=app, base=base))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(os.path.dirname(__file__), "templates"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


INSTALLED_APPS += [  # noqa
    'myopica.portfolio',
    'django.contrib.sitemaps',
    'raven.contrib.django.raven_compat',
]

MIDDLEWARE += [ # noqa
    'django.contrib.messages.middleware.MessageMiddleware',
]

ALLOWED_HOSTS += ['myopica.org']  # noqa
RETICULUM_URL = "https://reticulum.thraxil.org/"
USE_TZ = False
