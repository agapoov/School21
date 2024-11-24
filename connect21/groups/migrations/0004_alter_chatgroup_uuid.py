# Generated by Django 4.2.16 on 2024-11-10 15:47

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_chatgroup_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatgroup',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('1e5dc078-b3ee-4fb6-92c3-4427cd029894'), editable=False, unique=True),
        ),
    ]