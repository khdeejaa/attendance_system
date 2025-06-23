import csv
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Student, Class
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Attendance
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Lecturer
from .models import Student, Class
from .models import Subject
from .models import Attendance
from .forms import LecturerForm, StudentForm, SubjectForm
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count

# Custom Admin Login View
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        # Check if user is authenticated and is a superuser
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')  # Redirect to admin dashboard
        else:
            messages.error(request, "Invalid credentials or not authorized.")
    
    return render(request, 'admin_login.html')
# Update your admin_dashboard view in views.py

# Update your admin_dashboard view in views.py

def admin_dashboard(request):
    # Get counts for all models
    total_staff = Lecturer.objects.count()
    total_students = Student.objects.count()
    classes = Class.objects.all()  # Get all classes
    subjects = Subject.objects.all()  # Get all subjects
    
    # Calculate some additional statistics
    total_classes = classes.count()
    total_subjects = subjects.count()
    
    # Calculate ratios and averages
    student_staff_ratio = round(total_students / total_staff) if total_staff > 0 else 0
    avg_students_per_class = round(total_students / total_classes) if total_classes > 0 else 0
    subjects_per_staff = round(total_subjects / total_staff, 1) if total_staff > 0 else 0
    
    context = {
        'total_staff': total_staff,
        'total_students': total_students,
        'classes': classes,
        'subjects': subjects,
        'total_classes': total_classes,
        'total_subjects': total_subjects,
        'student_staff_ratio': student_staff_ratio,
        'avg_students_per_class': avg_students_per_class,
        'subjects_per_staff': subjects_per_staff,
        'show_add_lecturer_form': False
    }
    
    return render(request, 'admin_dashboard.html', context)
   
# Define the student login view
def student_login(request):
    """Student login view."""
    if request.method == 'POST':
        student_id = request.POST['student_id']
        password = request.POST['password']

        # Validate student credentials
        try:
            student = Student.objects.get(student_id=student_id, student_password=password)
            request.session['student_id'] = student.id
            request.session['student_name'] = student.student_name
            return redirect('student_dashboard')  # Redirect to the student's dashboard
        except Student.DoesNotExist:
            messages.error(request, 'Invalid Student ID or Password')
            return redirect('student_login')
    
    return render(request, 'student_login.html')

def staff_login(request):
    if request.method == "POST":
        staff_id = request.POST.get("username")  # or change to "staff_id" if you update the form
        staff_password = request.POST.get("password")  # or change to "staff_password"
        
        try:
            # Get lecturer by staff_id
            lecturer = Lecturer.objects.get(staff_id=staff_id)
            
            # Check if password matches
            if lecturer.staff_password == staff_password:
                # You can create a simple session or redirect directly
                # Store lecturer info in session
                request.session['staff_id'] = lecturer.staff_id
                request.session['staff_name'] = lecturer.staff_name
                request.session['is_staff_logged_in'] = True
                
                messages.success(request, f"Welcome {lecturer.staff_name}!")
                return redirect("staff_dashboard")
            else:
                messages.error(request, "Password is incorrect.")
        except Lecturer.DoesNotExist:
            messages.error(request, "Staff ID not found.")
        
        return redirect("staff_login")
    
    return render(request, "staff_login.html")
# Homepage view
def homepage(request):
    return render(request, 'homepage.html')




def student_homepage(request):
    student_id = request.session.get('student_id')
    
    if not student_id:
        return redirect('student_login')  # Redirect to login if student is not logged in
    
    student = Student.objects.get(id=student_id)
    
    # Fetch attendance records for the logged-in student
    attendance_records = Attendance.objects.filter(student=student)
    
    return render(request, 'student_homepage.html', {
        'attendance_records': attendance_records,
        'student_name': student.student_name,
        'student_id': student.student_id,
 # Assuming this is available in the Student model
    })

 # Temporarily disable CSRF validation for this view
from django.http import JsonResponse

from django.contrib.auth.models import User, Group

def add_lecturer(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        staff_name = request.POST.get('staff_name')
        staff_password = request.POST.get('staff_password')
        
        try:
            # Check if staff_id already exists
            if Lecturer.objects.filter(staff_id=staff_id).exists():
                messages.error(request, 'Staff ID already exists!')
                return render(request, 'add_lecturer.html')
            
            # Create Lecturer record
            lecturer = Lecturer.objects.create(
                staff_id=staff_id,
                staff_name=staff_name,
                staff_password=staff_password
            )
            
            messages.success(request, f'Lecturer {staff_name} added successfully! Login credentials: Staff ID = {staff_id}')
            
        except Exception as e:
            messages.error(request, f'Error adding lecturer: {str(e)}')
    
    return render(request, 'add_lecturer.html')

def list_lecturers(request):
    lecturers = Lecturer.objects.all()  # Fetch all lecturers from the database
    return render(request, 'list_lecturers.html', {'lecturers': lecturers})

def update_lecturer(request, lecturer_id):
    lecturer = get_object_or_404(Lecturer, id=lecturer_id)

    if request.method == 'POST':
        form = LecturerForm(request.POST, instance=lecturer)
        if form.is_valid():
            form.save()
            messages.success(request, "Lecturer details updated successfully!")
            return redirect('list_lecturers')  # Redirect to the list of lecturers
    else:
        form = LecturerForm(instance=lecturer)

    return render(request, 'update_lecturer.html', {'form': form})

def delete_lecturer(request, lecturer_id):
    lecturer = get_object_or_404(Lecturer, id=lecturer_id)
    lecturer.delete()
    messages.success(request, "Lecturer deleted successfully!")
    return redirect('list_lecturers')  # Redirect back to the list of lecturers
def students_for_class(request, subject_id, class_id):
    """Get students for a specific class and subject"""
    try:
        # Verify that the subject and class exist
        subject = Subject.objects.get(id=subject_id)
        class_instance = Class.objects.get(id=class_id)
        
        # Get all students assigned to this class
        students = Student.objects.filter(class_assigned=class_instance)
        
        # Format the response data
        student_data = []
        for student in students:
            student_data.append({
                'id': student.id,
                'student_id': student.student_id,
                'student_name': student.student_name
            })
        
        return JsonResponse(student_data, safe=False)
        
    except Subject.DoesNotExist:
        return JsonResponse({'error': 'Subject not found'}, status=404)
    except Class.DoesNotExist:
        return JsonResponse({'error': 'Class not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
def student_dashboard(request):
    """Display student's attendance records."""
    student_id = request.session.get('student_id')
    
    if not student_id:
        return redirect('student_login')  # Redirect to login if student is not logged in
    
    # Fetch attendance records for the logged-in student
    attendance_records = Attendance.objects.filter(student__id=student_id)
    
    return render(request, 'student_dashboard.html', {
        'attendance_records': attendance_records,
        'student_name': request.session.get('student_name'),  # Assuming the student's name is saved in the session
    })


def add_student(request):
    classes = Class.objects.all()  # Get all available classes
    if request.method == 'POST':
        student_id = request.POST['studentId']
        student_name = request.POST['studentName']
        student_password = request.POST['studentPassword']
        class_assigned = request.POST.get('class_assigned')  # Use .get() for safety
        
        print(f"Class assigned ID: {class_assigned}")  # Debugging line
        
        # Check if student ID already exists
        if Student.objects.filter(student_id=student_id).exists():
            messages.error(request, 'Student ID already exists!')
            return redirect('add_student')

        try:
            class_instance = Class.objects.get(id=class_assigned)
        except Class.DoesNotExist:
            messages.error(request, 'Class does not exist!')
            return redirect('add_student')
        
        # Create and save the student
        student = Student(
            student_id=student_id,
            student_name=student_name,
            student_password=student_password,
            class_assigned=class_instance  # Assign the class to the student
        )
        student.save()

        messages.success(request, 'Student added successfully!')
        return redirect('add_student')

    return render(request, 'add_student.html', {'classes': classes})



def list_students(request):
    students = Student.objects.all()
    return render(request, 'list_students.html', {'students': students})

def update_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    classes = Class.objects.all()  # Get all classes

    if request.method == 'POST':
        student.student_name = request.POST['studentName']
        student.student_password = request.POST['studentPassword']
        class_assigned = Class.objects.get(id=request.POST['class_assigned'])  # Get the selected class
        student.class_assigned = class_assigned
        student.save()

        messages.success(request, 'Student updated successfully!')
        return redirect('list_students')  # Redirect to the student list page

    return render(request, 'update_student.html', {'student': student, 'classes': classes})

def delete_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('list_students')  # Redirect back to the student list

    return render(request, 'delete_student.html', {'student': student})


def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new subject to the database
            messages.success(request, 'Subject added successfully!')
             # Redirect to the subject list page after adding
        else:
            messages.error(request, 'There was an error adding the subject. Please try again.')
    else:
        form = SubjectForm()

    return render(request, 'add_subject.html', {'add_lecturer': add_lecturer})


def delete_subject(request, subject_id):
    try:
        subject = Subject.objects.get(id=subject_id)
        subject.delete()
        messages.success(request, 'Subject deleted successfully!')
    except Subject.DoesNotExist:
        messages.error(request, 'Subject not found.')
    return redirect('list_subjects')

def list_subjects(request):
    subjects = Subject.objects.all()
    return render(request, 'list_subjects.html', {'subjects': subjects})

def update_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()  # Save the updated subject
            messages.success(request, 'Subject updated successfully!')
            return redirect('list_subjects')  # Redirect to the list of subjects
        else:
            messages.error(request, 'There was an error updating the subject.')
    else:
        form = SubjectForm(instance=subject)  # Pre-populate the form with the current subject data

    return render(request, 'update_subject.html', {'form': form, 'subject': subject})

import csv
from django.http import HttpResponse, JsonResponse
from django.db.models import Count

def admin_reports(request):
    """Main reports dashboard view"""
    return render(request, 'admin_reports.html')

def get_dashboard_data(request):
    """API endpoint to get dashboard statistics"""
    lecturers_count = Lecturer.objects.count()
    students_count = Student.objects.count()
    subjects_count = Subject.objects.count()
    
    # Calculate ratio
    ratio = round(students_count / lecturers_count) if lecturers_count > 0 else 0
    
    data = {
        'lecturers': lecturers_count,
        'students': students_count,
        'subjects': subjects_count,
        'ratio': ratio
    }
    
    return JsonResponse(data)

def download_overview_csv(request):
    """Download overview data as CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="system_overview_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Category', 'Count', 'Percentage'])
    
    lecturers_count = Lecturer.objects.count()
    students_count = Student.objects.count()
    subjects_count = Subject.objects.count()
    total = lecturers_count + students_count + subjects_count
    
    if total > 0:
        writer.writerow(['Lecturers', lecturers_count, f"{round((lecturers_count/total)*100)}%"])
        writer.writerow(['Students', students_count, f"{round((students_count/total)*100)}%"])
        writer.writerow(['Subjects', subjects_count, f"{round((subjects_count/total)*100)}%"])
    
    return response

def download_ratio_csv(request):
    """Download lecturer-student ratio as CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="lecturer_student_ratio_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Metric', 'Value'])
    
    lecturers_count = Lecturer.objects.count()
    students_count = Student.objects.count()
    ratio = round(students_count / lecturers_count) if lecturers_count > 0 else 0
    
    writer.writerow(['Total Students', students_count])
    writer.writerow(['Total Lecturers', lecturers_count])
    writer.writerow(['Student to Lecturer Ratio', f"{ratio}:1"])
    writer.writerow(['Students per Lecturer', ratio])
    
    return response

def download_complete_report(request):
    """Download complete system report as CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="complete_system_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Report Type', 'Category', 'Count', 'Percentage', 'Status'])
    
    lecturers_count = Lecturer.objects.count()
    students_count = Student.objects.count()
    subjects_count = Subject.objects.count()
    total = lecturers_count + students_count + subjects_count
    
    if total > 0:
        writer.writerow(['Staff', 'Active Lecturers', lecturers_count, f"{round((lecturers_count/total)*100)}%", 'Active'])
        writer.writerow(['Students', 'Enrolled Students', students_count, f"{round((students_count/total)*100)}%", 'Active'])
        writer.writerow(['Academic', 'Available Subjects', subjects_count, f"{round((subjects_count/total)*100)}%", 'Available'])
    
    return response

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Lecturer

def staff_login(request):
    if request.method == "POST":
        staff_id = request.POST.get("staff_id")
        staff_password = request.POST.get("staff_password")
        
        try:
            # Get lecturer by staff_id from your database
            lecturer = Lecturer.objects.get(staff_id=staff_id)
            
            # Check if password matches exactly
            if lecturer.staff_password == staff_password:
                # Store lecturer info in session for authentication
                request.session['staff_id'] = lecturer.staff_id
                request.session['staff_name'] = lecturer.staff_name
                request.session['is_staff_logged_in'] = True
                
                messages.success(request, f"Welcome {lecturer.staff_name}!")
                return redirect("staff_dashboard")
            else:
                messages.error(request, "Password is incorrect.")
        except Lecturer.DoesNotExist:
            messages.error(request, "Staff ID not found.")
        
        return redirect("staff_login")
    
    return render(request, "staff_login.html")

def staff_dashboard(request):
    # Check if staff is logged in
    if not request.session.get('is_staff_logged_in'):
        messages.error(request, "Please login first.")
        return redirect('staff_login')
    
    # Get staff info from session
    staff_name = request.session.get('staff_name', 'Staff')
    staff_id = request.session.get('staff_id', '')
    
    subjects = Subject.objects.all()
    classes = Class.objects.all()
    
    context = {
        'subjects': subjects,
        'classes' : classes,
        'staff_name': staff_name,
        'staff_id': staff_id,
    }
    return render(request, 'staff_dashboard.html', context)


def get_students_by_subject(request, subject_id):
    """API to get all students for a subject"""
    try:
        # Get all students (you can modify this to filter by subject if needed)
        students = Student.objects.all().values('id', 'student_id', 'student_name')
        return JsonResponse(list(students), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def mark_attendance(request):
    """Mark attendance for students"""
    if request.method == 'POST':
        try:
            subject_id = request.POST.get('subject_id')
            class_id = request.POST.get('class_id')  # Get class_id from form
            date = request.POST.get('date')
            time_slot = request.POST.get('time_slot')
            staff_id = request.session.get('staff_id')

            if not staff_id:
                messages.error(request, 'Please login first.')
                return redirect('staff_login')

            subject = Subject.objects.get(id=subject_id)
            class_instance = Class.objects.get(id=class_id)  # Get class instance

            # Filter students based on the selected class
            students = Student.objects.filter(class_assigned=class_instance)

            attendance_records = []

            for student in students:
                status = request.POST.get(f'attendance_{student.id}')
                if status:
                    # Check if attendance already exists for this date
                    attendance, created = Attendance.objects.get_or_create(
                        student=student,
                        subject=subject,
                        date=date,
                        time_slot=time_slot,
                        defaults={'status': status, 'marked_by': staff_id}
                    )

                    if not created:
                        # Update existing record
                        attendance.status = status
                        attendance.marked_by = staff_id
                        attendance.save()

                    attendance_records.append(attendance)

            messages.success(request, f'Attendance marked successfully for {len(attendance_records)} students!')
            return redirect('staff_dashboard')

        except Exception as e:
            messages.error(request, f'Error marking attendance: {str(e)}')
            return redirect('staff_dashboard')

    # If not POST, render the form with classes and subjects
    classes = Class.objects.all()  # Get all available classes
    subjects = Subject.objects.all()  # Get all available subjects
    return render(request, 'mark_attendance.html', {'classes': classes, 'subjects': subjects})

def admin_logout(request):
    """Logout admin user"""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('admin_login')

def staff_logout(request):
    """Logout staff member"""
    # Clear staff session data
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect('staff_login')

def student_logout(request):
    """Logout student user"""
    # Clear staff session data
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect('student_login')


from django.shortcuts import render
from django.http import JsonResponse
from .models import Attendance, Student, Subject


# Check for existing attendance records to prevent duplicates
def check_existing_attendance(request):
    subject_id = request.GET.get('subject_id')
    class_id = request.GET.get('class_id')
    date = request.GET.get('date')
    time_slot = request.GET.get('time_slot')
    
    if not all([subject_id, class_id, date, time_slot]):
        return JsonResponse({'error': 'Missing required parameters'}, status=400)
    
    try:
        # Get existing attendance records for this combination
        # Fixed field name: class_assigned_id instead of class_enrolled_id
        existing_records = Attendance.objects.filter(
            subject_id=subject_id,
            student__class_assigned_id=class_id,
            date=date,
            time_slot=time_slot
        ).select_related('student', 'subject')
        
        data = []
        for record in existing_records:
            data.append({
                'student_id': record.student.id,
                'student_name': record.student.student_name,
                'student_id_number': record.student.student_id,
                'status': record.status,
                'date': str(record.date),
                'time_slot': record.time_slot,
                'subject_code': record.subject.subject_code
            })
        
        return JsonResponse(data, safe=False)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Enhanced mark_attendance function with duplicate checking
@csrf_exempt
def mark_attendance(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        class_id = request.POST.get('class_id')
        date = request.POST.get('date')
        time_slot = request.POST.get('time_slot')
        
        if not all([subject_id, class_id, date, time_slot]):
            messages.error(request, '⚠️ All fields are required: Subject, Class, Date, and Time Slot.')
            return redirect('staff_dashboard')
        
        try:
            # Get all students in the class - Fixed field name
            students = Student.objects.filter(class_assigned_id=class_id)
            
            if not students.exists():
                messages.error(request, '⚠️ No students found in the selected class.')
                return redirect('staff_dashboard')
            
            new_records = []
            duplicate_count = 0
            processed_count = 0
            
            for student in students:
                attendance_key = f'attendance_{student.id}'
                status = request.POST.get(attendance_key)
                
                if status:  # Only process if status is provided
                    processed_count += 1
                    
                    # Check for existing record
                    existing_record = Attendance.objects.filter(
                        student=student,
                        subject_id=subject_id,
                        date=date,
                        time_slot=time_slot
                    ).first()
                    
                    if existing_record:
                        duplicate_count += 1
                        continue  # Skip this student
                    
                    # Create new attendance record
                    attendance = Attendance(
                        student=student,
                        subject_id=subject_id,
                        date=date,
                        time_slot=time_slot,
                        status=status
                    )
                    new_records.append(attendance)
            
            # Handle different scenarios with appropriate messages
            if processed_count == 0:
                messages.error(request, '⚠️ No students were selected for attendance marking.')
                return redirect('staff_dashboard')
            
            if duplicate_count == processed_count:
                # All students already have attendance marked
                messages.warning(request, f'⚠️ All {duplicate_count} student(s) already have attendance marked for this date and time slot. Cannot save duplicate records.')
                return redirect('staff_dashboard')
            
            # Bulk create new records
            if new_records:
                Attendance.objects.bulk_create(new_records)
                success_msg = f'✅ Attendance saved successfully for {len(new_records)} student(s).'
                if duplicate_count > 0:
                    success_msg += f' {duplicate_count} student(s) already had attendance marked and were skipped.'
                messages.success(request, success_msg)
            
        except Exception as e:
            # User-friendly error message instead of technical details
            messages.error(request, '❌ Failed to save attendance. Please check your selections and try again.')
            # Log the actual error for debugging (you can add logging here)
            print(f"Attendance save error: {str(e)}")  # For debugging
    
    return redirect('staff_dashboard')

# Fetch all attendance records for display
def all_attendance_records(request):
    records = Attendance.objects.select_related('student', 'subject', 'student__class_assigned').all()
    data = []
    for record in records:
        data.append({
            'id': record.id,
            'date': str(record.date),
            'student_id': record.student.student_id,
            'student_name': record.student.student_name,
            'class_name': record.student.class_assigned.class_name if record.student.class_assigned else 'N/A',
            'subject_code': record.subject.subject_code,
            'status': record.status,
            'time_slot': record.time_slot,
        })
    return JsonResponse(data, safe=False)

# Search attendance records by Student ID or Name
def search_attendance_records(request):
    query = request.GET.get('q', '').strip()
    if query:
        records = Attendance.objects.select_related('student', 'subject', 'student__class_assigned').filter(
            Q(student__student_id__icontains=query) | 
            Q(student__student_name__icontains=query)
        )
    else:
        records = Attendance.objects.none()  # No results if query is empty

    data = []
    for record in records:
        data.append({
            'id': record.id,
            'date': str(record.date),
            'student_id': record.student.student_id,
            'student_name': record.student.student_name,
            'class_name': record.student.class_assigned.class_name if record.student.class_assigned else 'N/A',
            'subject_code': record.subject.subject_code,
            'status': record.status,
            'time_slot': record.time_slot,
        })
    return JsonResponse(data, safe=False)

# Edit attendance record with proper AJAX handling
def edit_attendance_record(request, record_id):
    try:
        record = Attendance.objects.get(id=record_id)
        
        if request.method == 'POST':
            record.date = request.POST.get('date')
            record.status = request.POST.get('status')
            record.time_slot = request.POST.get('time_slot')
            record.save()

            # Return JSON response for AJAX calls
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'api/' in request.path:
                data = {
                    'success': True,
                    'message': 'Attendance record updated successfully',
                    'id': record.id,
                    'date': str(record.date),
                    'student_id': record.student.student_id,
                    'student_name': record.student.student_name,
                    'subject_code': record.subject.subject_code,
                    'status': record.status,
                    'time_slot': record.time_slot,
                }
                return JsonResponse(data)
            else:
                # For regular form submissions, redirect
                messages.success(request, "Attendance record updated successfully.")
                return redirect('staff_dashboard')
                
        else:
            # If not a POST request, send the current record for editing
            data = {
                'id': record.id,
                'date': str(record.date),
                'student_id': record.student.student_id,
                'student_name': record.student.student_name,
                'subject_code': record.subject.subject_code,
                'status': record.status,
                'time_slot': record.time_slot,
            }
            return JsonResponse(data, status=200)
            
    except Attendance.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Attendance record not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

# Get students for a specific class and subject
def students_for_class(request, subject_id, class_id):
    try:
        # Fixed field name: class_assigned_id instead of class_enrolled_id
        students = Student.objects.filter(class_assigned_id=class_id)
        
        if not students.exists():
            return JsonResponse({'error': 'No students found for this class'}, status=404)
        
        data = []
        for student in students:
            data.append({
                'id': student.id,
                'student_id': student.student_id,
                'student_name': student.student_name,
            })
        
        return JsonResponse(data, safe=False)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Delete attendance record
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_attendance_record(request, record_id):
    try:
        record = Attendance.objects.get(id=record_id)
        
        # Store student and subject info for the success message
        student_name = record.student.student_name
        subject_code = record.subject.subject_code
        
        record.delete()
        
        return JsonResponse({
            'success': True, 
            'message': f'Attendance record for {student_name} in {subject_code} deleted successfully'
        })
        
    except Attendance.DoesNotExist:
        return JsonResponse({
            'success': False, 
            'message': 'Attendance record not found'
        }, status=404)
        
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': f'Error deleting record: {str(e)}'
        }, status=500)