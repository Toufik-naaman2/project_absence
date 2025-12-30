from django.db import models
from django.conf import settings
import uuid

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'}, related_name='courses')

    def __str__(self):
        return f"{self.code} - {self.name}"

class Session(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sessions')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    # Token for QR code - unique to this session
    token = models.CharField(max_length=64, default=uuid.uuid4, unique=True, editable=False)
    
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.course.code} - {self.date}"
