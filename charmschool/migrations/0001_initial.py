# Generated by Django 3.2.5 on 2021-07-13 23:06

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import gdstorage.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', models.CharField(max_length=3000)),
                ('subject', models.CharField(max_length=100)),
                ('due_date', models.DateTimeField()),
                ('max_score', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('นาย', 'นาย'), ('นางสาว', 'นางสาว')], max_length=6)),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=200)),
                ('student_id', models.IntegerField()),
                ('email_ref', models.EmailField(max_length=254)),
                ('group_ref', models.CharField(max_length=25)),
                ('score', models.PositiveIntegerField(default=10, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['group_ref', 'student_id'],
            },
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('นาย', 'นาย'), ('นางสาว', 'นางสาว')], max_length=6)),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[('IS', 'อาจารย์ผู้สอน'), ('TA', 'นักศึกษาผู้ช่วยสอน')], max_length=2)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Course_Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', models.CharField(max_length=3000)),
                ('subject', models.CharField(max_length=100)),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='charmschool.instructor')),
                ('groups', models.ManyToManyField(to='auth.Group')),
            ],
            options={
                'verbose_name': 'Course Content',
                'verbose_name_plural': 'Course Contents',
            },
        ),
        migrations.CreateModel(
            name='Course_Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', models.CharField(max_length=3000)),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='charmschool.instructor')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='charmschool.course_content')),
            ],
            options={
                'verbose_name': 'Course Comment',
                'verbose_name_plural': 'Course Comments',
            },
        ),
        migrations.CreateModel(
            name='Classwork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submit_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('work', models.FileField(null=True, storage=gdstorage.storage.GoogleDriveStorage(), upload_to='classwork/<django.db.models.fields.related.OneToOneField>')),
                ('score', models.IntegerField(null=True)),
                ('graded', models.BooleanField(default=False)),
                ('assignment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='charmschool.assignment')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='assignment',
            name='author',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='charmschool.instructor'),
        ),
    ]
