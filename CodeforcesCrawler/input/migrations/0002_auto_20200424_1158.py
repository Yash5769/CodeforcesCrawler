# Generated by Django 3.0.5 on 2020-04-24 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('input', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='time_table',
            name='time',
            field=models.DateTimeField(),
        ),
    ]
