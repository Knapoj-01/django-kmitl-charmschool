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
        