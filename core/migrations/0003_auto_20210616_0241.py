# Generated by Django 3.1.5 on 2021-06-16 02:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210608_1353'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='inviter',
            new_name='inviter_user_id',
        ),
    ]
