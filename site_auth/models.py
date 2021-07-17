from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def is_student(self):
        return hasattr(self,'student')
    def is_instructor(self):
        return hasattr(self,'instructor')

