from django.core.exceptions import PermissionDenied

def check_group_visiblilty(content, user):
    for group in user.groups.all():
        if group in content.visible_by.all():
            break
        raise PermissionDenied
    return True
def check_access_permission(group,user):
    if not group in user.groups.all():
        raise PermissionDenied
    else: return True

