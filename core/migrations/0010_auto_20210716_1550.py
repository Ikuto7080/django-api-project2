# Generated by Django 3.1.5 on 2021-07-16 15:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0009_auto_20210716_1540'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='connection',
            name='following_user',
        ),
        migrations.AddField(
            model_name='connection',
            name='followings',
            field=models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
    ]
