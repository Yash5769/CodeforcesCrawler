# Generated by Django 3.0.5 on 2020-04-25 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('input', '0004_verdicts'),
    ]

    operations = [
        migrations.CreateModel(
            name='level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('val', models.IntegerField()),
            ],
        ),
    ]
