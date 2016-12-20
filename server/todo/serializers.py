from .models import List, Todo
from rest_framework import serializers


class TodoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'todo',)


class ListSerializer(serializers.HyperlinkedModelSerializer):
    todos = TodoSerializer(many=True, read_only=True)
    class Meta:
        model = List
        fields = ('id', 'name', 'todos')
