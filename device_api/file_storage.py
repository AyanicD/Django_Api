from django.utils import timezone
from django.conf import settings


def upload_remote_path(instance, filename):
    parent_folder = "raven"
    today = timezone.localtime(timezone.now()).date()
    folder_name = instance.id

    return f"{parent_folder}/{today}/{folder_name}-{filename}"
