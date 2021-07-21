# Generated by Django 3.2.5 on 2021-07-21 02:10

import charmschool.models
from django.db import migrations, models
import gdstorage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('charmschool', '0022_alter_classwork_work'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classwork',
            name='work',
            field=models.FileField(blank=True, null=True, storage=gdstorage.storage.GoogleDriveStorage(), upload_to=charmschool.models.get_upload_path),
        ),
    ]
