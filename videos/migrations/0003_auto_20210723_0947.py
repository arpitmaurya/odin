# Generated by Django 3.1.6 on 2021-07-23 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_auto_20210723_0534'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='url',
            new_name='uuid',
        ),
    ]