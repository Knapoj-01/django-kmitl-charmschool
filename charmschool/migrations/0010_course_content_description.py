# Generated by Django 3.2.5 on 2021-07-15 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charmschool', '0009_auto_20210715_1836'),
    ]

    operations = [
        migrations.AddField(
            model_name='course_content',
            name='description',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
