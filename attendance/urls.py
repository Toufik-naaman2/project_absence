from django.urls import path
from . import views

urlpatterns = [
    path('mark/<str:token>/', views.mark_attendance, name='mark_attendance'),
    path('history/', views.student_history, name='student_history'),
    path('scan/', views.scan_qr, name='scan_qr'),
    path('manual/<int:session_id>/', views.mark_manual_attendance, name='mark_manual_attendance'),
]
