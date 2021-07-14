from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.utils import timezone
from gdstorage.storage import GoogleDriveStorage
gd_storage = GoogleDriveStorage()

gender_choices = [
    ('นาย', 'นาย'),
    ('นางสาว', 'นางสาว'),
]
type_choices = [
    ('IS', 'อาจารย์ผู้สอน'),
    ('TA', 'นักศึกษาผู้ช่วยสอน')
]
class Student(models.Model):
    class Meta:
        ordering = ['group_ref', 'student_id']
        
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(max_length=6, choices=gender_choices)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=200)
    student_id = models.IntegerField()
    email_ref = models.EmailField()
    group_ref = models.CharField(max_length=25)
    score = models.PositiveIntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return str(self.user)

class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(max_length=6, choices=gender_choices)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=200)
    type = models.CharField(max_length=2, choices=type_choices)

    def __str__(self):
        return str(self.user)

class Content_Base(models.Model):
    class Meta:
        abstract = True

    author = models.OneToOneField(Instructor, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=3000)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return self.subject

class Course_Content(Content_Base):
    groups = models.ManyToManyField(Group)
    class Meta:
        verbose_name = 'Course Content'
        verbose_name_plural = 'Course Contents'

class Assignment(Content_Base):
    due_date = models.DateTimeField()
    max_score = models.IntegerField()

class Course_Comment(Content_Base):
    class Meta:
        verbose_name = 'Course Comment'
        verbose_name_plural = 'Course Comments'
    subject = models.ForeignKey(Course_Content, on_delete=models.CASCADE)


class Classwork(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignment = models.OneToOneField(Assignment, on_delete=models.CASCADE)
    submit_date = models.DateTimeField(default=timezone.now)
    work = models.FileField(upload_to='classwork/{}'.format(str(assignment)), storage=gd_storage, null=True)
    score = models.IntegerField(null=True)
    graded = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + str(self.assignment)

class GroupData(models.Model):
    class Meta:
        verbose_name_plural='Group Data'
    weekday_choices=[
        ('จันทร์', 'จันทร์'),
        ('อังคาร', 'อังคาร'),
        ('พุธ', 'พุธ'),
        ('พฤหัสบดี', 'พฤหัสบดี'),
        ('ศุกร์', 'ศุกร์'),
        ('เสาร์', 'เสาร์'),
        ('อาทิตย์', 'อาทิตย์')
    ]
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    description = models.CharField(max_length=256)
    start_time = models.TimeField()
    end_time = models.TimeField()
    study_on = models.CharField(choices=weekday_choices, max_length=10)
    place = models.CharField(max_length=100)

    def __str__(self):
        return str(self.group)