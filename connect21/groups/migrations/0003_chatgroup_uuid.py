# Generated by Django 4.2.7 on 2024-11-10 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_chatmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatgroup',
            name='uuid',
            field=models.UUIDField(default=0, editable=False, unique=True),
            preserve_default=False,
        ),
    ]