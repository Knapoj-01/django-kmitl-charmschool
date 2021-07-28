from django.core.exceptions import PermissionDenied
from .models import GroupData
from .utils import *
from django.shortcuts import get_object_or_404

class SuperuserRequiredMixin:
    def dispatch(self,request,*args, **kwargs):
        if self.request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

class GetInfoMixin:
    def get_context_data(self, group_pk,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        groupdata = get_object_or_404(GroupData ,pk=group_pk)
        context['is_instructor'] = self.request.user.is_instructor()
        context['is_student'] = self.request.user.is_student()
        context["groupdata"] = groupdata
        context['instructors'] = groupdata.group.user_set.filter(instructor__id__isnull=False).order_by('-instructor__type')
        check_access_permission(groupdata.group,self.request.user)
        return context