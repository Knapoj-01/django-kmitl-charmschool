# Generated by Django 3.2.5 on 2021-07-15 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('charmschool', '0010_course_content_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='charmschool.instructor'),
        ),
        migrations.AlterField(
            model_name='course_comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='charmschool.instructor'),
        ),
        migrations.AlterField(
            model_name='course_content',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='charmschool.instructor'),
        ),
    ]
