# Generated by Django 3.0.3 on 2020-02-29 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photohireapp', '0004_auto_20200228_0229'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Hotel',
        ),
        migrations.AddField(
            model_name='person',
            name='profile_views',
            field=models.IntegerField(default=0),
        ),
    ]