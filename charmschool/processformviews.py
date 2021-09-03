from django.db.models.fields import PositiveBigIntegerField
from django.http.response import HttpResponse
from google.auth.transport import Request
from charmschool.importdataviews import import_data
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import redirect
from .forms import *
from .googleapiutils import *
from .models import Classwork
from django.contrib import messages

class AddContentView(LoginRequiredMixin, View):
    def post(self,request,*args, **kwargs):
        if 'assignment' in request.POST.keys():
            form = AddAssignmentForm(request.POST,user_groups_queryset= request.user.groups.all())
        elif 'content' in request.POST.keys():
            form = AddContentForm(request.POST,user_groups_queryset= request.user.groups.all())
        else: return redirect('classroom', group_pk=kwargs.get('group_pk'))
        if form.is_valid():
            model = form.save(commit=False)
            model.author = request.user.instructor
            model.save()
            model.visible_by.set(request.POST.getlist('visible_by'))
        return redirect('classroom', group_pk= kwargs.get('group_pk'))

class EditContentView(LoginRequiredMixin, View):
    def post(self,request,**kwargs):
        if 'assignment_pk' in kwargs.keys():
            form = AddAssignmentForm(
                request.POST,user_groups_queryset= request.user.groups.all(),
                instance = Assignment.objects.get(pk = kwargs.get('assignment_pk')))
        elif 'content_pk' in kwargs.keys():
            form = AddContentForm(
                request.POST,user_groups_queryset= request.user.groups.all(),
                instance = Course_Content.objects.get(pk = kwargs.get('content_pk')))
        else: return redirect('../')
        if form.is_valid():
            model = form.save(commit=False)
            model.save()
            model.visible_by.set(request.POST.getlist('visible_by'))
        return redirect('../')

class DeleteContentView(LoginRequiredMixin,View):
    def post(self,request,*args, **kwargs):
        if 'assignment_pk' in kwargs.keys():
            Assignment.objects.get(pk = kwargs.get('assignment_pk')).delete()
        elif 'content_pk' in kwargs.keys():
            Course_Content.objects.get(pk = kwargs.get('content_pk')).delete()
        else: return redirect('classroom', group_pk=kwargs.get('group_pk'))
        return redirect('classroom', group_pk=kwargs.get('group_pk'))

class SubmitClassworkView(LoginRequiredMixin,View):
    def post(self,request,group_pk, assignment_pk,*args, **kwargs):
        classwork = Classwork.objects.filter(
            student = request.user.student,
            assignment__id = assignment_pk
            )
        if not classwork:
            form = AddClassWorkForm(request.POST)
            if form.is_valid():
                model = form.save(request, assignment_pk)
                if 'file_id' in request.POST.keys():
                    file_list = []
                    id_list = request.POST.getlist('file_id')
                    name_list = request.POST.getlist('file_name')
                    for id, name in zip(id_list, name_list):
                        file_list.append({'name': name, 'id': id})
                    model.works = json.dumps(file_list)
                    model.save()
                    messages.success(request, r'<b>สำเร็จ:</b> ท่านได้ทำการส่งการบ้าน และแนบไฟล์สำเร็จแล้ว')
                else: messages.warning(request, r'<b>เตือน:</b> ท่านได้ทำการส่งงานสำเร็จ แต่ไม่พบไฟล์แนบ หากนี่เป็นข้อผิดพลาด กรุณาส่งงานใหม่')
            else: messages.error(request, r'<b>พบข้อผิดพลาด</b>: ไม่สามารถส่งงานได้')
        return redirect('../')

class UnsubmitClassworkView(LoginRequiredMixin, View):
    def post(self,request,group_pk, assignment_pk,*args, **kwargs):
        if 'delete' in request.POST.keys():
            classwork = Classwork.objects.filter(
                student = request.user.student,
                assignment__id = assignment_pk
                )
            if classwork:
                classwork.delete()
                messages.success(request, r'สำเร็จ: ท่านได้ทำการยกเลิกการส่งงานแล้ว')
        return redirect('../')

class GradeClassworkView(LoginRequiredMixin,View):
    def post(self,request,*args, **kwargs):
        if 'score' and 'classwork_id' in request.POST.keys():
            for id, score, feedback in zip(
                request.POST.getlist('classwork_id'), 
                request.POST.getlist('score'), 
                request.POST.getlist('feedback')):
                if score:
                    classwork = Classwork.objects.get(pk = id)
                    classwork.score = score
                    classwork.feedback = feedback
                    classwork.graded = True
                    classwork.save()   
        messages.success(request, r'สำเร็จ: บันทึกคะแนนและข้อคิดเห็นของผู้สอนแล้ว')
        return redirect(request.POST.get('success_url'))

