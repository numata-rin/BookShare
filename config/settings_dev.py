# 開発環境固有の設定ファイル

from .settings_common import *

SECRET_KEY = 'django-insecure-l%3)(&x+7ia+bf=zm$adwj@#)9fh5)pd&@rqr6*+2brr@#83#6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,

  'loggers': {
    # Djangoが利用するロガー
    'django': {
      'handlers': ['console'],
      'level': 'INFO',
    },
    # diaryアプリケーションが利用するロガー
    'diary': {
      'handlers': ['console'],
      'level': 'DEBUG',
    },
  },

  # ハンドラの設定
  'handlers': {
    'console': {
      'level': 'DEBUG',
      'class': 'logging.StreamHandler',
      'formatter': 'dev'
    },
  },

  # フォーマッタの設定
  'formatters': {
    'dev': {
      'format': '\t'.join([
        '%(asctime)s',
        '[%(levelname)s]',
        '%(pathname)s(Line:%(lineno)d)',
        '%(message)s'
      ])
    },
  }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')