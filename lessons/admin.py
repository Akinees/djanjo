from django.contrib import admin
from .models import Category, Lesson, LessonResource

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']
    search_fields = ['name']

class LessonResourceInline(admin.TabularInline):
    model = LessonResource
    extra = 1

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'duration_minutes', 'points', 'created_at']
    list_filter = ['category', 'difficulty', 'created_at']
    search_fields = ['title', 'description']
    inlines = [LessonResourceInline]
    ordering = ['category', 'order', 'title']