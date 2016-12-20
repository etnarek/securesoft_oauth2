from .models import List, Todo
from rest_framework import serializers


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'url', 'todo')



class TodoSerializerdetail(serializers.ModelSerializer):
    list_url = serializers.HyperlinkedIdentityField(source="todo_list", view_name="list-detail")
    class Meta:
        model = Todo
        fields = ('id', 'url', 'todo', 'todo_list', "list_url")


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ('id', 'url', 'name')

    def create(self, validated_data):
        name = validated_data.pop("name")
        user = self.context["request"].user
        return List.objects.create(name=name, user=user)

class ListSerializerDetail(serializers.ModelSerializer):
    todos = TodoSerializer(many=True, read_only=True)
    class Meta:
        model = List
        fields = ('id', 'url', 'name', 'todos')
