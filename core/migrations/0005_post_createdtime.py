# Generated by Django 3.1.6 on 2021-05-26 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210517_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='createdtime',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
