from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import AttendanceRecord
from academic.models import Session

@login_required
def mark_attendance(request, token):
    if not request.user.is_student():
        messages.error(request, "Only students can mark attendance.")
        return redirect('dashboard')

    session = get_object_or_404(Session, token=token)
    
    # Check session expiration (30 minutes from start time)
    now = timezone.now()
    # Combine date and time (timezone aware)
    session_start = timezone.make_aware(timezone.datetime.combine(session.date, session.start_time))
    expiration_time = session_start + timezone.timedelta(minutes=30)
    
    if now > expiration_time:
        return render(request, 'attendance/error.html', {'message': "This QR code has expired (30 minute limit exceeded)."})

    # Check if already marked
    if AttendanceRecord.objects.filter(student=request.user, session=session).exists():
        messages.info(request, "You have already marked attendance for this session.")
        return redirect('dashboard')

    # Create record
    AttendanceRecord.objects.create(
        student=request.user,
        session=session,
        status='present'
    )
    
    messages.success(request, f"Attendance marked for {session.course.name}")
    return render(request, 'attendance/success.html', {'session': session})

@login_required
def student_history(request):
    if not request.user.is_student():
        return redirect('dashboard')
        
    records = AttendanceRecord.objects.filter(student=request.user).order_by('-timestamp')
    return render(request, 'attendance/student_history.html', {'records': records})

@login_required
def scan_qr(request):
    if not request.user.is_student():
        messages.error(request, "Only students can scan QR codes.")
        return redirect('dashboard')
    return render(request, 'attendance/scan_qr.html')

from accounts.models import User

@login_required
def mark_manual_attendance(request, session_id):
    if not request.user.is_teacher() and not request.user.is_superuser:
        messages.error(request, "Only teachers can mark attendance manually.")
        return redirect('dashboard')
        
    session = get_object_or_404(Session, pk=session_id)
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        student = get_object_or_404(User, pk=student_id)
        
        if not AttendanceRecord.objects.filter(student=student, session=session).exists():
            AttendanceRecord.objects.create(student=student, session=session, status='present')
            messages.success(request, f"Marked {student.username} as present.")
        else:
            messages.warning(request, f"{student.username} is already marked as present.")
            
    return redirect('session_detail', pk=session_id)
