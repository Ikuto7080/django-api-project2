# Generated by Django 3.1.5 on 2021-06-16 02:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210616_0241'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='inviter_user_id',
            new_name='inviter',
        ),
    ]
