# Generated by Django 3.2.5 on 2021-07-17 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charmschool', '0017_auto_20210717_1907'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='score',
        ),
    ]
