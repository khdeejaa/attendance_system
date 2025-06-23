# forms.py
from django import forms
from .models import Lecturer, Student, Subject
from .models import Attendance

class LecturerForm(forms.ModelForm):
    class Meta:
        model = Lecturer  # Reference to the Lecturer model
        fields = ['staff_id', 'staff_name', 'staff_password']  # Fields that should be included in the form

#studentForm 
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student  # Ensure Student model is correctly referenced
        fields = ['student_id', 'student_name', 'student_password']  # Define fields for student form

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_code', 'subject_name']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'subject', 'date', 'status', 'time_slot']