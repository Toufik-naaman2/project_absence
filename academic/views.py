from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Session, Course
from .forms import SessionForm
import qrcode
from django.http import HttpResponse
from io import BytesIO

@login_required
def create_session(request):
    if request.method == 'POST':
        form = SessionForm(request.POST, user=request.user)
        if form.is_valid():
            session = form.save(commit=False)
            session.created_by = request.user
            session.save()
            return redirect('session_detail', pk=session.pk)
    else:
        form = SessionForm(user=request.user)
    return render(request, 'academic/create_session.html', {'form': form})

from django.core.paginator import Paginator

@login_required
def session_list(request):
    sessions = Session.objects.all()
    if request.user.role == 'teacher':
        sessions = sessions.filter(course__teacher=request.user)
    
    # Filter by date
    date_filter = request.GET.get('date')
    if date_filter:
        sessions = sessions.filter(date=date_filter)
        
    sessions = sessions.order_by('-date', '-start_time')
    
    # Pagination
    paginator = Paginator(sessions, 10) # 10 sessions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'academic/session_list.html', {'page_obj': page_obj, 'date_filter': date_filter})

from accounts.models import User

@login_required
def session_detail(request, pk):
    session = get_object_or_404(Session, pk=pk)
    attendance_records = session.attendancerecord_set.all().select_related('student')
    students = User.objects.filter(role='student') if request.user.role in ['teacher', 'admin'] or request.user.is_superuser else None
    
    context = {
        'session': session,
        'attendance_records': attendance_records,
        'students': students
    }
    return render(request, 'academic/session_detail.html', context)

@login_required
def generate_qr(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    # URL that student scans
    attendance_url = request.build_absolute_uri(f'/attendance/mark/{session.token}/')
    
    img = qrcode.make(attendance_url)
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)
    return HttpResponse(buffer, content_type='image/png')

@login_required
def session_attendance_list(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    # Ensure only the teacher of the course can view this (or admin)
    if request.user != session.course.teacher and not request.user.is_admin():
         return redirect('dashboard')

    attendances = session.attendances.select_related('student').all()
    return render(request, 'academic/session_attendance_list.html', {'session': session, 'attendances': attendances})
