from django.contrib import admin
from .models import *

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user','group_ref','student_id', 'gender', 'name', 'surname']
    list_filter = ['group_ref', 'gender']
    
@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['user','gender','name','surname', 'type']

@admin.register(Course_Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['author','subject','pub_date']
@admin.register(Course_Comment)
class CommentAdmin(ContentAdmin):
    pass

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['subject','pub_date','due_date']

@admin.register(Classwork)
class ClassworkAdmin(admin.ModelAdmin):
    list_display= ['assignment','submit_date', 'score']

@admin.register(GroupData)
class GroupDataAdmin(admin.ModelAdmin):
    list_display=['group','study_on', 'start_time','end_time', 'place']
