# Generated by Django 3.2.5 on 2021-07-28 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charmschool', '0023_alter_classwork_work'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classwork',
            name='work',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
