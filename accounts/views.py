from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from attendance.models import AttendanceRecord
from academic.models import Course, Session
from django.db.models import Count

@login_required
def dashboard(request):
    user = request.user
    if user.role == 'student':
        return redirect('student_dashboard')
    elif user.role == 'teacher':
        return redirect('teacher_dashboard')
    elif user.role == 'admin':
        return redirect('admin:index')
    return render(request, 'base.html')

@login_required
def student_dashboard(request):
    # Get courses the student has attended at least once
    records = AttendanceRecord.objects.filter(student=request.user)
    course_ids = records.values_list('session__course', flat=True).distinct()
    
    courses_data = [] # Names
    attendance_data = [] # Percentages
    
    for cid in course_ids:
        course = Course.objects.get(pk=cid)
        total_sessions = Session.objects.filter(course=course).count()
        my_attendance = records.filter(session__course=course).count()
        
        if total_sessions > 0:
            percentage = (my_attendance / total_sessions) * 100
        else:
            percentage = 0
            
        courses_data.append(course.name)
        attendance_data.append(round(percentage, 1))

    context = {
        'chart_labels': courses_data,
        'chart_data': attendance_data,
        'recent_records': records.order_by('-timestamp')[:5]
    }
    return render(request, 'dashboard_student.html', context)

@login_required
def teacher_dashboard(request):
    courses = Course.objects.filter(teacher=request.user)
    
    course_names = []
    total_attendances = []
    
    for course in courses:
        # Total check-ins for this course across all sessions
        count = AttendanceRecord.objects.filter(session__course=course).count()
        course_names.append(course.code)
        total_attendances.append(count)
        
    context = {
        'courses': courses,
        'chart_labels': course_names,
        'chart_data': total_attendances,
        'total_checkins': sum(total_attendances)
    }
    return render(request, 'dashboard_teacher.html', context)

from .forms import ProfileUpdateForm
from django.contrib import messages

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})
