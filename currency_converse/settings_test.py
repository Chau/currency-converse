# coding: utf-8

import logging

from settings import *


# Отключаем логгирование при выполнении тестов
logging.disable(logging.CRITICAL)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': ':memory:',
}

# Убираем debug toolbar из подключаемых приложений
if 'debug_toolbar' in INSTALLED_APPS:
    INSTALLED_APPS = tuple(app for app in INSTALLED_APPS if app != 'debug_toolbar')
    MIDDLEWARE = tuple(
        mw for mw in MIDDLEWARE if mw != 'debug_toolbar.middleware.DebugToolbarMiddleware'
    )

RATES_FNAME = os.path.join(BASE_DIR, 'exchangerates', 'tests', 'data', 'last_rates.json')