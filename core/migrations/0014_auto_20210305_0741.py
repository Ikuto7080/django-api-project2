# Generated by Django 3.1.5 on 2021-03-05 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_igpost_place_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='igpost',
            name='latitude',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='igpost',
            name='location_name',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='igpost',
            name='longitude',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]