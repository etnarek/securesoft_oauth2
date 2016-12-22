from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied

from .models import List, Todo
from rest_framework import viewsets, permissions
from .serializers import ListSerializer, TodoSerializer, ListSerializerDetail, TodoSerializerdetail
from server.permissions import IsOwner


class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    permission_classes = (IsOwner, permissions.IsAuthenticated)

    def list(self, request):
        user = self.request.user
        self.queryset = self.queryset.filter(user=user)
        return super(ListViewSet, self).list(request)

    def retrieve(self, *args, **kwargs):
        self.serializer_class = ListSerializerDetail
        return super(ListViewSet, self).retrieve(*args, **kwargs)

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = (IsOwner, permissions.IsAuthenticated)

    def list(self, request):
        user = self.request.user
        self.queryset = self.queryset.filter(todo_list__user=user)
        return super(TodoViewSet, self).list(request)

    def retrieve(self, *args, **kwargs):
        self.serializer_class = TodoSerializerdetail
        return super(TodoViewSet, self).retrieve(*args, **kwargs)

    def create(self, request):
        list_id = request.POST.get("todo_list")
        lists = get_object_or_404(List, pk=list_id)
        if lists.user != request.user:
            raise PermissionDenied
        self.serializer_class = TodoSerializerdetail

        return super(TodoViewSet, self).create(request)
