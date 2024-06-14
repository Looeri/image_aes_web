from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Django의 설정 모듈을 Celery의 기본으로 설정합니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imageEncrypt.settings')

app = Celery('imageEncrypt')

# 여기에 Django 설정 파일에서 설정을 로드합니다.
app.config_from_object('django.conf:settings', namespace='CELERY')

# 장고의 모든 등록된 앱 설정에서 task 모듈을 검색합니다.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete-old-images-every-day': {
        'task': 'app.tasks.delete_old_images_task',
        'schedule': crontab(hour=0, minute=0),  # 매일 자정에 실행
    },
}