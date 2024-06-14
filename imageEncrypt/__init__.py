from __future__ import absolute_import, unicode_literals

# 이 코드를 사용하면 Celery 앱이 Django가 시작될 때 함께 로드됩니다.
from .celery import app as celery_app

__all__ = ('celery_app',)

#celery -A imageEncrypt worker --loglevel=info
#celery -A imageEncrypt beat --loglevel=info