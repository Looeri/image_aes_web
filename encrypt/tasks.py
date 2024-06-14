from celery import shared_task
from imageEncrypt.utils import delete_old_images
from django.conf import settings
import os

@shared_task
def delete_old_images_task():
    folder_path = os.path.join(settings.MEDIA_ROOT, 'encrypt_images')
    delete_old_images(folder_path)