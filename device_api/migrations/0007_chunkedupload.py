# Generated by Django 4.1.5 on 2023-02-15 05:26

import device_api.file_storage
import device_api.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('device_api', '0006_attachment'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChunkedUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_id', models.CharField(default=device_api.models.generate_upload_id, editable=False, max_length=32, unique=True)),
                ('file', models.FileField(blank=True, max_length=255, null=True, upload_to=device_api.file_storage.upload_remote_path)),
                ('filename', models.CharField(max_length=255)),
                ('offset', models.BigIntegerField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('completed_on', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chunked_uploads', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
