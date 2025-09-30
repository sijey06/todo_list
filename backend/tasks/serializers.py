from rest_framework import serializers

from .models import Category, Task


class CategorySerializer(serializers.ModelSerializer):
    """Серилайзер категорий."""

    class Meta:
        model = Category
        fields = ('id', 'title',)


class TaskSerializer(serializers.ModelSerializer):
    """Серилайзер задач."""

    category = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all())

    class Meta:
        model = Task
        fields = '__all__'
