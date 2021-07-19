from django.db.models.fields import PositiveBigIntegerField
from charmschool.importdataviews import import_data
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import redirect
from .forms import *

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