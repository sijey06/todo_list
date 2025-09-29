from rest_framework import viewsets

from .models import Category, Task
from .serializers import CategorySerializer, TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """Вьюсет для задач."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        telegram_user_id = self.request.query_params.get('telegram_user_id')
        if telegram_user_id is not None:
            return Task.objects.filter(telegram_user_id=telegram_user_id)
        return Task.objects.all()


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет для категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
