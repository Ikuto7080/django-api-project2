# Generated by Django 3.1.5 on 2021-07-12 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_account_postkit_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='postkit_url',
            field=models.ImageField(blank=True, null=True, upload_to='invitepicture/'),
        ),
        migrations.AlterField(
            model_name='account',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profilepic/'),
        ),
        migrations.AlterField(
            model_name='postimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='postimage/'),
        ),
    ]
