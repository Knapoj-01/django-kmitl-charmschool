from django.db.models.fields import PositiveBigIntegerField
from charmschool.importdataviews import import_data
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import redirect
from .forms import *
from .googleapiutils import *
from .models import Classwork

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
        if classwork:
            instance = classwork[0]
            form = AddClassWorkForm(request.POST, instance=instance)
        else : 
            form = AddClassWorkForm(request.POST)
        if form.is_valid():
            id_list = None
            if request.FILES:
                service = token_authentication(request)
                charmschool = create_folder_if_not_exists(service, 'Charmschool')
                assignments_folder = create_folder_if_not_exists(
                    service, 'assignments', charmschool.get('id')
                    )
                folder = create_folder_if_not_exists(
                    service, str(assignment_pk), assignments_folder.get('id')
                    )
                files = request.FILES.getlist('works')
                id_list = upload_user_contents(service,files, request, folder.get('id'))
            form.save(request, assignment_pk, id_list)
        return redirect('../')

class GradeClassworkView(LoginRequiredMixin,View):
    def post(self,request,group_pk, assignment_pk,*args, **kwargs):
        if 'score' in request.POST.keys():
            classwork = Classwork.objects.get(pk = request.POST.get('classwork_id'))
            classwork.score = request.POST.get('score')
            classwork.feedback = request.POST.get('feedback')
            classwork.graded = True
            classwork.save()
        return redirect(request.POST.get('success_url'))