# Generated by Django 3.0.3 on 2020-03-21 23:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photohireapp', '0010_auto_20200322_0413'),
    ]

    operations = [
        migrations.RenameField(
            model_name='social',
            old_name='pinterest_id',
            new_name='facebook_id',
        ),
    ]
