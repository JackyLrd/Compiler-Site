from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Task(models.Model):
    task_name = models.CharField(max_length=30, default='task')
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
