# Generated by Django 3.2.5 on 2021-07-21 01:18

from django.db import migrations, models
import gdstorage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('charmschool', '0020_alter_classwork_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classwork',
            name='work',
            field=models.FileField(blank=True, null=True, storage=gdstorage.storage.GoogleDriveStorage(), upload_to='KMITL-CharmWeb/classwork/<django.db.models.fields.related.ForeignKey>'),
        ),
    ]
