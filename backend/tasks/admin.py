from django.contrib import admin

from .models import Category, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date')
    search_fields = ('title', )
    list_filter = ('category', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
