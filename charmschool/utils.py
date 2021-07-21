from django.core.exceptions import PermissionDenied

def check_group_visiblilty(content, user):
    for group in user.groups.all():
        for content_group in content.visible_by.all():
            if group == content_group:
                return True
    raise PermissionDenied
    
def check_access_permission(group,user):
    if not group in user.groups.all():
        raise PermissionDenied
    else: return True

