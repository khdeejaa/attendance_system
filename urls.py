from django.urls import path
from . import views  # Import views from the SATS app

urlpatterns = [
    path('admin/login/', views.admin_login, name='admin_login'),  # Admin login
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard
    path('student/login/', views.student_login, name='student_login'),  # Student login
    path('staff/login/', views.staff_login, name='staff_login'),  # Add staff login route here
    path('admin/lecturer/add/', views.add_lecturer, name='add_lecturer'),
    path('admin/lecturer/list/', views.list_lecturers, name='list_lecturers'),
    path('admin/lecturer/update/<int:lecturer_id>/', views.update_lecturer, name='update_lecturer'),
    path('admin/lecturer/delete/<int:lecturer_id>/', views.delete_lecturer, name='delete_lecturer'),
    path('admin/student/add/', views.add_student, name='add_student'),
    path('admin/student/list/', views.list_students, name='list_students'),
    path('admin/lecturer/add/', views.add_lecturer, name='add_lecturer'),
    path('admin/lecturer/list/', views.list_lecturers, name='list_lecturers'),
    path('update/<int:student_id>/', views.update_student, name='update_student'),
    path('delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('add_subject/', views.add_subject, name='add_subject'),
    path('delete_subject/<int:subject_id>/', views.delete_subject, name='delete_subject'),
    path('add_subject/', views.add_subject, name='add_subject'),
    path('list_subjects/', views.list_subjects, name='list_subjects'),
    path('update_subject/<int:subject_id>/', views.update_subject, name='update_subject'),
    path('add-lecturer/', views.add_lecturer, name='add_lecturer'),
    path('reports/', views.admin_reports, name='admin_reports'),
    path('api/dashboard-data/', views.get_dashboard_data, name='dashboard_data'),
    path('download/overview-csv/', views.download_overview_csv, name='download_overview_csv'),
    path('download/ratio-csv/', views.download_ratio_csv, name='download_ratio_csv'),
    path('download/complete-report/', views.download_complete_report, name='download_complete_report'),
    path('staff-login/', views.staff_login, name='staff_login'),
    path('update-lecturer/<int:lecturer_id>/', views.update_lecturer, name='update_lecturer'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('api/students-by-subject/<int:subject_id>/', views.get_students_by_subject, name='get_students_by_subject'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('staff-logout/', views.staff_logout, name='staff_logout'),
    path('student-logout/', views.student_logout, name='student_logout'),
    path('api/all-attendance-records/', views.all_attendance_records, name='all_attendance_records'),
    path('api/search-attendance-records/', views.search_attendance_records, name='search_attendance_records'),
    path('api/attendance-record/<int:record_id>/', views.edit_attendance_record, name='edit_attendance_record'),
    path('api/students-by-subject/<str:subject_code>/', views.get_students_by_subject, name='get_students_by_subject'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('edit-attendance/<int:record_id>/', views.edit_attendance_record, name='edit_attendance'),
    path('api/students-by-subject/<int:subject_id>/', views.get_students_by_subject, name='get_students_by_subject'),
    path('api/students-for-class/<int:subject_id>/<int:class_id>/', views.students_for_class, name='students_for_class'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/homepage/', views.student_homepage, name='student_homepage'),
    path('api/all-attendance-records/', views.all_attendance_records, name='all_attendance_records'),
    path('api/search-attendance-records/', views.search_attendance_records, name='search_attendance_records'),
    path('api/attendance-record/<int:record_id>/', views.edit_attendance_record, name='edit_attendance'),
    # Remove duplicate - keep only one
    path('api/attendance-record/<int:record_id>/', views.edit_attendance_record, name='edit_attendance_record'),
    path('api/delete-attendance-record/<int:record_id>/', views.delete_attendance_record, name='delete_attendance_record'),
    
    # Fix the search endpoint name to match frontend JavaScript
    path('api/search-student-records/', views.search_attendance_records, name='search_student_records'),
    path('api/check-existing-attendance/', views.check_existing_attendance, name='check_existing_attendance'),
    
    # Attendance management
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('api/all-attendance-records/', views.all_attendance_records, name='all_attendance_records'),
    path('api/search-student-records/', views.search_attendance_records, name='search_student_records'),
    
    # Edit and delete attendance
    path('api/attendance-record/<int:record_id>/', views.edit_attendance_record, name='edit_attendance_record'),
    path('api/delete-attendance-record/<int:record_id>/', views.delete_attendance_record, name='delete_attendance_record'),
    
    # Student data (FIXED to use class_assigned_id)
    path('api/students-for-class/<int:subject_id>/<int:class_id>/', views.students_for_class, name='students_for_class'),
    path('api/students-by-subject/<str:subject_code>/', views.get_students_by_subject, name='get_students_by_subject'),
    path('api/students-by-subject/<int:subject_id>/', views.get_students_by_subject, name='get_students_by_subject'),
    
    # Student pages
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/homepage/', views.student_homepage, name='student_homepage'),

]


