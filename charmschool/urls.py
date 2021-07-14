from django.urls import path
from django.views.generic import TemplateView
from .views import *
from .adddata import*

urlpatterns = [
    path('', IndexView.as_view(extra_context={'title_name': 'Charm School KMITL'})),
    path('dashboard/', DashboardView.as_view(extra_context={'title_name': 'Dashboard'}), name='dashboard'),
    path('dashboard/creategroup/', AddGroupView.as_view()),
]
