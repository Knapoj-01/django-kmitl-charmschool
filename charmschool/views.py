from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
from .mixins import *
from .utils import *

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
        if self.request.user.is_student():
            context['classworks'] = Classwork.objects.filter(student=self.request.user.student)
            context['assignments'] = Assignment.objects.filter(
                visible_by__id__exact=group.pk
                ).exclude(
                    classwork__in= Classwork.objects.filter(student=self.request.user.student)
                    ).order_by('due_date','pub_date')
        else:
            context['assignments'] = Assignment.objects.filter(
                visible_by__id__exact=group.pk
                ).order_by('due_date','pub_date')
            context['assignment_form'] = AddAssignmentForm(user_groups_queryset= self.request.user.groups.all())
            context['content_form'] = AddContentForm(user_groups_queryset= self.request.user.groups.all())
        context['course_contents'] = Course_Content.objects.filter(visible_by__id__exact=group.pk).order_by('-pub_date')
        return context
    
class ContentView(GetInfoMixin, LoginRequiredMixin, TemplateView):
    template_name = 'charmschool/content/index.html'
    def get_context_data(self,group_pk,content_pk, **kwargs):
        context = super().get_context_data(group_pk,**kwargs)
        content = get_object_or_404(Course_Content, pk = content_pk)      
        context["content"] = content
        context["comments"] = Course_Comment.objects.filter(subject__id = content_pk)
        context['form'] = AddCommentForm
        check_group_visiblilty(content, self.request.user)
        return context
    def post(self, request,content_pk,*args, **kwargs):
        if request.POST.keys() >= {"delete", "comment_pk"}:
            Course_Comment.objects.get(pk = int(request.POST['comment_pk'])).delete()
        form = AddCommentForm(request.POST)
        if form.is_valid():
            form.save(request,content_pk)
        return redirect(self.request.path_info)

class AssignmentView(GetInfoMixin,LoginRequiredMixin,TemplateView):
    template_name = 'charmschool/assignment/index.html'
    def get_context_data(self,group_pk, assignment_pk, **kwargs):
        context = super().get_context_data(group_pk,**kwargs)
        context["assignment"] = Assignment.objects.get(pk = assignment_pk)
        context['form'] = AddClassWorkForm
        if self.request.user.is_instructor():
            return_list = []
            return_classwork = []
            student_list = Student.objects.filter(
                group_ref=group_pk
                )
            for obj in student_list:
                if obj.classwork_set:
                    classwork = obj.classwork_set.filter(assignment__id = assignment_pk)
                    if classwork:
                        element = [obj , classwork[0]]
                        return_classwork.append(element)
                    else: return_list.append([obj])
            context['classwork_list'] = return_classwork+return_list
        else:
            classwork_queryset = Classwork.objects.filter(
            assignment__id = assignment_pk, student = self.request.user.student
            )
            if classwork_queryset: context['classwork'] = classwork_queryset[0]
        return context
    def post(self,request,group_pk, assignment_pk,*args, **kwargs):
        form = AddClassWorkForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request, assignment_pk)
        elif 'score' in request.POST.keys():
            classwork = Classwork.objects.get(pk = request.POST.get('classwork_id'))
            classwork.score = request.POST.get('score')
            classwork.save()
        return redirect(self.request.path_info)

class GroupMembersView(GetInfoMixin,LoginRequiredMixin,ListView):
    template_name = 'charmschool/group/members.html'
    model = Student
    context_object_name = 'members'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(self.kwargs.get('group_pk'),**kwargs)
        return context
    def get_queryset(self):
        queryset = Student.objects.filter(group_ref=self.kwargs.get('group_pk')).order_by('student_id')
        return queryset
    
    