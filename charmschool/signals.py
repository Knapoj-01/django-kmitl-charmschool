from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from .models import Student
from django.contrib.auth.models import Group

@receiver(user_logged_in)
def user_signed_up_signal_handler(request, user, **kwargs):
    db = Student.objects.filter(email_ref = user.email)
    for object in db:
        if object.user ==None:
            object.user = user
            object.save()
        gr = Group.objects.get(pk = int(object.group_ref))
        if not gr in user.groups.all():
            user.groups.add(gr)

 
    
