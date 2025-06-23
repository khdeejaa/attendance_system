# models.py
from django.db import models
from django.utils import timezone

class Lecturer(models.Model):
    staff_id = models.CharField(max_length=50, unique=True)
    staff_name = models.CharField(max_length=100)
    staff_password = models.CharField(max_length=100)

def __str__(self):
        return f"{self.staff_id} - {self.staff_name}"

class Class(models.Model):
    class_name = models.CharField(max_length=100)  # e.g., "Mathematics 101"
    
    def __str__(self):
        return self.class_name  # Return only the class_name


# Student model
class Student(models.Model):
    student_id = models.CharField(max_length=10)
    student_name = models.CharField(max_length=100)
    student_password = models.CharField(max_length=100)

    # Add a foreign key field to link the student to a class
    class_assigned = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.student_name
    
class Subject(models.Model):
    subject_code = models.CharField(max_length=10, unique=True)  # Unique subject code
    subject_name = models.CharField(max_length=100)  # Name of the subject

    def __str__(self):
        return self.subject_name
    
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    marked_by = models.CharField(max_length=50)  # Staff ID who marked
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['student', 'subject', 'date', 'time_slot']
    
    def __str__(self):
        return f"{self.student.student_name} - {self.subject.subject_code} - {self.date} - {self.status}"