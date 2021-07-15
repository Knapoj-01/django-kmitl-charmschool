from django.urls import path
from django.views.generic import TemplateView
from .views import *
from .importdataviews import*

urlpatterns = [
    path('', IndexView.as_view(extra_context={'title_name': 'Charm School KMITL'})),
    path('dashboard/', DashboardView.as_view(extra_context={'title_name': 'หน้าหลักผู้ใช้'}), name='dashboard'),
    path('dashboard/creategroup/', AddGroupView.as_view()),
    path('group/<int:group_pk>/', ClassroomView.as_view(extra_context={'title_name': 'ห้องเรียน'}), name='classroom'),
    path('group/<int:group_pk>/content/<int:content_pk>/', ContentView.as_view(extra_context={'title_name': 'เนื้อหา'}), name='content'),
    #path('assignment/<int:pk>/', AssignmentView.as_view())
]
