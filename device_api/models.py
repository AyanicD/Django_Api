from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords
from device_api.file_storage import upload_remote_path

import uuid
import hashlib
from datetime import timedelta
from django.core.files.uploadedfile import UploadedFile
from django.conf import settings

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    history = HistoricalRecords()

class Device(models.Model):
    name = models.CharField(max_length=100,unique=True)
    type = models.CharField(max_length=25)
    history = HistoricalRecords()
    timestamp = models.DateTimeField(default=timezone.now)
    employee = models.ForeignKey(Employee, blank=True, null=True, on_delete=models.SET_NULL)

class Attachment(models.Model):
    name = models.CharField(max_length=100,unique=True)
    file = models.FileField(upload_to=upload_remote_path, null=True, blank=True)

def generate_upload_id():
    return uuid.uuid4().hex

class AbstractChunkedUpload(models.Model):
    """
    Base chunked upload model. This model is abstract (doesn't create a table
    in the database).
    Inherit from this model to implement your own.
    """

    upload_id = models.CharField(max_length=32, unique=True, editable=False,
                                 default=generate_upload_id)
    file = models.FileField(max_length=255, upload_to=upload_remote_path,
                            null=True, blank=True)
    filename = models.CharField(max_length=255)
    offset = models.BigIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(null=True, blank=True)

    @property
    def expires_on(self):
        return self.created_on + timedelta(days=1)

    @property
    def expired(self):
        return self.expires_on <= timezone.now()

    @property
    def md5(self):
        if getattr(self, '_md5', None) is None:
            md5 = hashlib.md5()
            for chunk in self.file.chunks():
                md5.update(chunk)
            self._md5 = md5.hexdigest()
        return self._md5

    def delete(self, delete_file=True, *args, **kwargs):
        if self.file:
            storage, path = self.file.storage, self.file.path
        super(AbstractChunkedUpload, self).delete(*args, **kwargs)
        if self.file and delete_file:
            storage.delete(path)

    def __str__(self):
        return u'<%s - upload_id: %s - bytes: %s - status: %s>' % (
            self.filename, self.upload_id, self.offset, self.status)

    def append_chunk(self, chunk, chunk_size=None, save=True):
        self.file.close()
        with open(self.file.path, mode='ab') as file_obj:  # mode = append+binary
            file_obj.write(chunk.read())  # We can use .read() safely because chunk is already in memory

        if chunk_size is not None:
            self.offset += chunk_size
        elif hasattr(chunk, 'size'):
            self.offset += chunk.size
        else:
            self.offset = self.file.size
        self._md5 = None  # Clear cached md5
        if save:
            self.save()
        self.file.close()  # Flush

    def get_uploaded_file(self):
        self.file.close()
        self.file.open(mode='rb')  # mode = read+binary
        return UploadedFile(file=self.file, name=self.filename,
                            size=self.offset)

    class Meta:
        abstract = True


class ChunkedUpload(AbstractChunkedUpload):
    """
    Default chunked upload model.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chunked_uploads',
        null=True,
        blank=True
    )
    ## null and black editable
