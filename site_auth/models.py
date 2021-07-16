from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def is_student(self):
        return self.student_set.exists()
    def is_instructor(self):
        return hasattr(self,'instructor')

