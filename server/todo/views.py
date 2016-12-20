from django.shortcuts import render

from .models import List, Todo
from rest_framework import viewsets
from .serializers import ListSerializer, TodoSerializer, ListSerializerDetail
from server.permissions import IsOwner


class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    permission_classes = (IsOwner, )

    def get_queryset(self):
        user = self.request.user
        return List.objects.filter(user=user)

    def retrieve(self, *args, **kwargs):
        print("hello")
        self.serializer_class = ListSerializerDetail
        return super(ListViewSet, self).retrieve(*args, **kwargs)

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = (IsOwner, )

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(todo_list__user=user)
