from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.utils import timezone
from gdstorage.storage import GoogleDriveStorage
gd_storage = GoogleDriveStorage()

gender_choices = [
    ('นาย', 'นาย'),
    ('นาง', 'นาง'),
    ('นางสาว', 'นางสาว'),
    ('อาจารย์', 'อาจารย์'),
    ('ผู้ช่วยศาสตราจารย์', 'ผู้ช่วยศาสตราจารย์'),
    ('รองศาสตราจารย์', 'รองศาสตราจารย์'),
    ('ศาสตราจารย์', 'ศาสตราจารย์'),
]
type_choices = [
    ('อาจารย์ผู้สอน', 'อาจารย์ผู้สอน'),
    ('นักศึกษาผู้ช่วยสอน', 'นักศึกษาผู้ช่วยสอน')
]
class Student(models.Model):
    class Meta:
        ordering = ['group_ref', 'student_id']
        
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    gender = models.CharField(max_length=20, choices=gender_choices)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=200)
    student_id = models.IntegerField()
    email_ref = models.EmailField()
    group_ref = models.IntegerField()
    score = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return str(self.user)

class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group)
    gender = models.CharField(max_length=30, choices=gender_choices)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=200)
    type = models.CharField(max_length=30, choices=type_choices)

    def __str__(self):
        return str(self.user)

class Content_Base(models.Model):
    class Meta:
        abstract = True

    author = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    visible_by = models.ManyToManyField(Group)
    pub_date = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=3000)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return str(self.subject)

class Course_Content(Content_Base):
    description = models.CharField(max_length=256, null=True)
    class Meta:
        verbose_name = 'Course Content'
        verbose_name_plural = 'Course Contents'

class Assignment(Content_Base):
    due_date = models.DateTimeField()
    max_score = models.IntegerField()

class Course_Comment(Content_Base):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    visible_by = None
    class Meta:
        verbose_name = 'Course Comment'
        verbose_name_plural = 'Course Comments'
    subject = models.ForeignKey(Course_Content, on_delete=models.CASCADE)


class Classwork(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    message = models.CharField(max_length=500, null=True)
    submit_date = models.DateTimeField(default=timezone.now)
    work = models.FileField(upload_to='classwork/{}'.format(str(assignment)), storage=gd_storage, null=True, blank=True)
    score = models.IntegerField(null=True)
    graded = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + ' '+ str(self.assignment)

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
    description = models.CharField('คำอธิบาย',max_length=256)
    start_time = models.TimeField('เริ่มเรียน')
    end_time = models.TimeField('เลิกเรียน')
    study_on = models.CharField('วันที่เรียน',choices=weekday_choices, max_length=10)
    place = models.CharField('สถานที่เรียน', max_length=100)

    def __str__(self):
        return str(self.group)