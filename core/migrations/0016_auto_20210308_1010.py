# Generated by Django 3.1.5 on 2021-03-08 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_account_line_use_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='line_use_id',
            new_name='line_user_id',
        ),
    ]
