from .models import List, Todo
from rest_framework import serializers


class TodoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'url', 'todo', 'todo_list')


class ListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = List
        fields = ('id', 'url', 'name')

    def create(self, validated_data):
        name = validated_data.pop("name")
        user = self.context["request"].user
        l = List.objects.create(name=name, user=user)

class ListSerializerDetail(serializers.HyperlinkedModelSerializer):
    todos = TodoSerializer(many=True, read_only=True)
    class Meta:
        model = List
        fields = ('id', 'url', 'name', 'todos')

    def create(self, validated_data):
        name = validated_data.pop("name")
        user = self.context["request"].user
        l = List.objects.create(name=name, user=user)
        return l
