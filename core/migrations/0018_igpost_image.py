# Generated by Django 3.1.5 on 2021-03-09 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20210309_0113'),
    ]

    operations = [
        migrations.AddField(
            model_name='igpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]