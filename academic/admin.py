from django.contrib import admin
from .models import Course, Session

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'teacher')
    list_filter = ('teacher',)
    search_fields = ('name', 'code')

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('course', 'date', 'start_time', 'end_time', 'is_active')
    list_filter = ('course', 'is_active', 'date')
