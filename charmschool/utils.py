from django.http import HttpResponseForbidden
def check_group_visiblilty(content, user):
    for group in user.groups.all():
        if group in content.visible_by.all():
            break
        return HttpResponseForbidden
    return True