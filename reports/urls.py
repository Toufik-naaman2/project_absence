from django.urls import path
from . import views

urlpatterns = [
    path('export/csv/', views.export_attendance_csv, name='export_attendance_csv'),
    path('export/pdf/', views.export_attendance_pdf, name='export_attendance_pdf'),
    path('export/session/<int:session_id>/pdf/', views.export_single_session_pdf, name='export_single_session_pdf'),
]
