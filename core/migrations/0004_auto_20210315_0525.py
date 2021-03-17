# Generated by Django 3.1.5 on 2021-03-15 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_fbpost_google_info'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fbpost',
            name='type',
        ),
        migrations.RemoveField(
            model_name='igpost',
            name='type',
        ),
        migrations.AddField(
            model_name='igpost',
            name='google_info',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
