# Django settings for myopica project.
import os.path
from thraxilsettings.shared import common

app = 'myopica'
base = os.path.dirname(__file__)

locals().update(common(app=app, base=base))

INSTALLED_APPS += [  # noqa
    'myopica.portfolio',
    'django.contrib.sitemaps',
]

ALLOWED_HOSTS += ['myopica.org']  # noqa
