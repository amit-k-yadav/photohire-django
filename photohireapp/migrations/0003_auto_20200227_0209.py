# Generated by Django 3.0.3 on 2020-02-26 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photohireapp', '0002_auto_20200227_0012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='url',
            field=models.CharField(max_length=5000),
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]