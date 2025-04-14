from .settings import *

DEBUG = True

ALLOWED_HOSTS = ['*']  # pro lokální testování klidně otevřené

# Nepoužíváme cachování ani jiné optimalizace
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Volitelné: logování výjimek
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
