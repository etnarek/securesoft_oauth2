from django.db import models
from django.conf import settings

# Create your models here.

class List(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name


class Todo(models.Model):
    todo = models.CharField(max_length=255)
    todo_list = models.ForeignKey(List, on_delete=models.CASCADE)

    def __str__(self):
        return self.todo
