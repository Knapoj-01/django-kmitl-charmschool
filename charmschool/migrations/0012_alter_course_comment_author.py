# Generated by Django 3.2.5 on 2021-07-15 19:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('charmschool', '0011_auto_20210715_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course_comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
