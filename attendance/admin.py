from django.contrib import admin
from .models import AttendanceRecord

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'session', 'status', 'timestamp')
    list_filter = ('session__course', 'status', 'timestamp')
    search_fields = ('student__username',)
