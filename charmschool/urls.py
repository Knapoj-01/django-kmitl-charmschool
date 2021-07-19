from django.urls import path
from .views import *
from .importdataviews import*
from .processformviews import *

urlpatterns = [
    path('', IndexView.as_view(extra_context={'title_name': 'Charm School KMITL'})),
    path('dashboard/', DashboardView.as_view(extra_context={'title_name': 'หน้าหลักผู้ใช้'}), name='dashboard'),
    path('dashboard/creategroup/', AddGroupView.as_view()),
    path('group/<int:group_pk>/', ClassroomView.as_view(extra_context={'title_name': 'ห้องเรียน'}), name='classroom'),
    path('group/<int:group_pk>/addcontent/', AddContentView.as_view()),
    path('group/<int:group_pk>/members/', GroupMembersView.as_view(extra_context={'title_name': 'สมาชิกในกลุ่มเรียน'}), name='members'),
    path('group/<int:group_pk>/content/<int:content_pk>/', ContentView.as_view(extra_context={'title_name': 'เนื้อหา'}), name='content'),
    path('group/<int:group_pk>/assignment/<int:assignment_pk>/', AssignmentView.as_view(extra_context={'title_name': 'การบ้าน'}), name='assignment'),
    path('group/<int:group_pk>/content/<int:content_pk>/editcontent/',EditContentView.as_view()),
    path('group/<int:group_pk>/assignment/<int:assignment_pk>/editcontent/', EditContentView.as_view()),
    path('group/<int:group_pk>/content/<int:content_pk>/deletecontent/', DeleteContentView.as_view()),
    path('group/<int:group_pk>/assignment/<int:assignment_pk>/deletecontent/', DeleteContentView.as_view()),
]
