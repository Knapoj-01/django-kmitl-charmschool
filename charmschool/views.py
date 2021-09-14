from django.core import paginator
from django.http import request
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.utils.timezone import localtime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from copy import deepcopy
from .models import *
from .forms import *
from .mixins import *
from .utils import *
from .googleapiutils import *
from django.contrib import messages

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
        content_all = Course_Content.objects.filter(visible_by__id__exact=group.pk).order_by('-pub_date')
        if self.request.user.is_student():
            context['classworks'] = Classwork.objects.filter(student=self.request.user.student)
            context['assignments'] = Assignment.objects.filter(
                visible_by__id__exact=group.pk
                ).exclude(
                    classwork__in= Classwork.objects.filter(student=self.request.user.student)
                    ).order_by('due_date','pub_date')
            context['course_contents'] = content_all.exclude(private = True)[:3]
        else:
            context['assignments'] = Assignment.objects.filter(
                visible_by__id__exact=group.pk
                ).order_by('due_date','pub_date')
            context['assignment_form'] = AddAssignmentForm(user_groups_queryset= self.request.user.groups.all())
            context['content_form'] = AddContentForm(user_groups_queryset= self.request.user.groups.all())
            context['course_contents'] = content_all[:3]
        return context
    
class ContentListView(GetInfoMixin, LoginRequiredMixin, TemplateView):
    template_name = 'charmschool/group/contentlist.html'
    def get_context_data(self,group_pk,**kwargs):
        context = super().get_context_data(group_pk, **kwargs)
        content_all = Course_Content.objects.filter(visible_by__id__exact=group_pk).order_by('-pub_date')
        if self.request.user.is_student(): 
            content_all = content_all.exclude(private = True)
        if 'private' in self.request.GET.keys():
            content_all = content_all.filter(private = bool(self.request.GET.get('private')))
        if 'q' in self.request.GET.keys():
            contents = content_all.filter(subject__contains = self.request.GET.get('q'))
        else:
            contents = content_all
        context["contents"] = contents
        return context

class ContentView(GetInfoMixin, LoginRequiredMixin, TemplateView):
    template_name = 'charmschool/content/index.html'
    def get_context_data(self,group_pk,content_pk, **kwargs):
        context = super().get_context_data(group_pk,**kwargs)
        content = get_object_or_404(Course_Content, pk = content_pk)  
        if self.request.user.is_student() and content.private == True:
            raise PermissionDenied
        context["content"] = content
        context["comments"] = Course_Comment.objects.filter(subject__id = content_pk)
        context['form'] = AddCommentForm
        if self.request.user.is_instructor():
            context['editcontentform'] = AddContentForm(
                instance = content,
                user_groups_queryset= self.request.user.groups.all()
                )
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
        assignment = get_object_or_404(Assignment, pk = assignment_pk)
        context["assignment"] = assignment
        if self.request.user.is_instructor():
            assignment_form = deepcopy(assignment)
            assignment_form.due_date = localtime(assignment_form.due_date).strftime("%Y-%m-%dT%H:%M")
            form =  AddAssignmentForm(
                instance = assignment_form, user_groups_queryset= self.request.user.groups.all()
                )
            context['form'] = form
            return_list = []
            return_classwork = []
            student_list = Student.objects.filter(
                group_ref=group_pk
                )
            for obj in student_list:
                if obj.classwork_set:
                    classwork = obj.classwork_set.filter(assignment__id = assignment_pk)
                    if classwork:
                        element = [obj , classwork_queryset_deserial(classwork)[0]]
                        return_classwork.append(element)
                    else: return_list.append([obj])
            paginator = Paginator(return_classwork + return_list, 10)
            # Paginator Settings
            page = self.request.GET.get('page', 1)
            try:
                clist = paginator.page(page)
            except PageNotAnInteger:
                clist = paginator.page(1)
            except EmptyPage:
                clist = paginator.page(paginator.num_pages)
            context['classwork_list'] = clist
        if self.request.user.is_student():
            classwork_queryset = Classwork.objects.filter(
            assignment__id = assignment_pk, student = self.request.user.student
            )
            if classwork_queryset: 
                classwork = classwork_queryset_deserial(classwork_queryset)[0]
                context['classwork'] = classwork
            else:
                service, creds = token_authentication(self.request)
                charmschool = create_folder_if_not_exists(service, 'Charmschool')
                assignments_folder = create_folder_if_not_exists(
                    service, 'assignments', charmschool.get('id')
                    )
                folder = create_folder_if_not_exists(
                    service, str(assignment_pk), assignments_folder.get('id')
                    )
                context['target_folder'] = folder.get('id')
                context['token'] = creds.token
                context['form'] = AddClassWorkForm
        return context
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
                    service, creds = token_authentication(request)
                    try: 
                        for id, name in zip(id_list, name_list):
                            file_list.append({'name': name, 'id': id})
                            modify_permissions(service, id)
                        model.works = json.dumps(file_list)
                        messages.success(request, r'<b>สำเร็จ:</b> ท่านได้ทำการส่งการบ้าน และแนบไฟล์สำเร็จแล้ว')
                    except:
                        print('Error')
                        messages.error(request, r'<b>พบข้อผิดพลาด</b>: ไม่สามารถส่งงานได้ (Permission Error)')
                else: messages.warning(request, r'<b>เตือน:</b> ท่านได้ทำการส่งงานสำเร็จ แต่ไม่พบไฟล์แนบ หากนี่เป็นข้อผิดพลาด กรุณาส่งงานใหม่')
                model.save()
            else: messages.error(request, r'<b>พบข้อผิดพลาด</b>: ไม่สามารถส่งงานได้ (Form invalid)')
        else: messages.error(request, r'<b>พบข้อผิดพลาด</b>: ไม่สามารถส่งงานได้ (Row Exists)')
        return redirect('./')


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
    
class MemberProfileView(GetInfoMixin, LoginRequiredMixin, TemplateView):
    template_name = 'charmschool/group/profile.html'
    def get_context_data(self,group_pk, student_pk, **kwargs):
        context = super().get_context_data(group_pk,**kwargs)
        object = get_object_or_404(Student, pk = student_pk)  
        queryset = object.classwork_set.all()
        if 'q' in self.request.GET.keys():
            queryset = queryset.filter(assignment__subject__contains = self.request.GET.get('q'))
        queryset = classwork_queryset_deserial(queryset.order_by('assignment__due_date'))
        context["member"] = object
        context['classworks'] = queryset
        return context
    
    