from typing import List
from django.db import models
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from . models import Assignment, Course_Comment, Course_Content, GroupData, Instructor
from .forms import *
from .mixins import *

class IndexView(TemplateView):
    template_name='charmschool/index.html'
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
    
class DashboardView(LoginRequiredMixin, ListView):
    login_url='/'
    context_object_name = 'groups'
    template_name = 'charmschool/dashboard.html'
    
    def get_queryset(self):
        queryset = self.request.user.groups.all().order_by('name')
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddGroupDataForm
        return context
    
class ClassroomView(GetInfoMixin, LoginRequiredMixin, TemplateView):
    template_name = 'charmschool/group/index.html'
    def get_context_data(self, group_pk, **kwargs):
        context = super().get_context_data(group_pk,**kwargs)
        group = GroupData.objects.get(pk=group_pk)
        context['assignments'] = Assignment.objects.filter(visible_by__id__exact=group.pk).order_by('due_date','pub_date')
        context['course_contents'] = Course_Content.objects.filter(visible_by__id__exact=group.pk).order_by('pub_date')
        return context
    
class ContentView(GetInfoMixin, LoginRequiredMixin, TemplateView):
    template_name = 'charmschool/content/index.html'
    def get_context_data(self,group_pk,content_pk, **kwargs):
        context = super().get_context_data(group_pk,**kwargs)
        context["content"] = Course_Content.objects.get(pk = content_pk)
        context["comments"] = Course_Comment.objects.filter(subject__id = content_pk)
        context['form'] = AddCommentForm
        return context
    def post(self, request,content_pk,*args, **kwargs):
        if request.POST.keys() >= {"delete", "comment_pk"}:
            Course_Comment.objects.get(pk = int(request.POST['comment_pk'])).delete()
        form = AddCommentForm(request.POST)
        if form.is_valid():
            form.save(request,content_pk)
        return redirect(self.request.path_info)



