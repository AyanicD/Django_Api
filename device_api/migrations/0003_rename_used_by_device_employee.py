# Generated by Django 4.1.5 on 2023-02-01 05:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device_api', '0002_alter_device_history'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='used_by',
            new_name='employee',
        ),
    ]