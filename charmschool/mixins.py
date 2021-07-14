from django.core.exceptions import PermissionDenied

class SuperuserRequiredMixin:
    def dispatch(self,request,*args, **kwargs):
        if self.request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied