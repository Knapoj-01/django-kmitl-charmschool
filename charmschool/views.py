from django.db import models
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

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
    


