from django.core.exceptions import PermissionDenied
from .models import GroupData, Instructor

class SuperuserRequiredMixin:
    def dispatch(self,request,*args, **kwargs):
        if self.request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

class GetInfoMixin:
    def get_context_data(self, group_pk,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        group = GroupData.objects.get(pk=group_pk)
        context['is_instructor'] = self.request.user.is_instructor()
        context['is_student'] = self.request.user.is_student()
        context["groupdata"] = group
        context['instructors'] = Instructor.objects.filter(groups__id__exact=group.pk).order_by('-type')
        return context