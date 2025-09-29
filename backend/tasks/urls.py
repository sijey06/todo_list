from django.urls import include, path
from rest_framework.routers import DefaultRouter

from tasks.views import CategoryViewSet, TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'categories', CategoryViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
