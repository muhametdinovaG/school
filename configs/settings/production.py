from .base import *

DEBUG = False

WEBPACK_LOADER['DEFAULT'].update({
    'BUNDLE_DIR_NAME': 'dist/',
    'STATS_FILE': 'webpack-stats-prod.json'
})

INSTALLED_APPS.append('raven.contrib.django.raven_compat')
RAVEN_CONFIG = {
    'dsn': 'http://2d2a2cd388d145399ec0212e6dc0c95a:baf53110e4d44d80a4bb4f74a1909d06@sentry.lo.ufanet.ru/85',
}

LOGGING['loggers']['django']['handlers'].append('sentry')
LOGGING['loggers']['django']['level'] = 'INFO'

LOGGING['loggers']['modules']['handlers'].append('sentry')
LOGGING['loggers']['modules']['level'] = 'INFO'
