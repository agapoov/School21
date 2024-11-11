# Generated by Django 4.2.16 on 2024-11-10 15:48

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_alter_chatgroup_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatgroup',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
