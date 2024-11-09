from django.urls import path
from . import views

urlpatterns = [
    # **Students CRUD**
    path('api/students/', views.student_list, name='get_students'),  # Fetch all students
    path('api/students/create/', views.create_student, name='create_student'),  # Create a new student
    path('api/students/<int:student_id>/', views.student_detail, name='student_detail'),  # Get student details
    path('api/students/<int:student_id>/update/', views.update_student, name='update_student'),  # Update a student
    path('api/students/<int:student_id>/delete/', views.delete_student, name='delete_student'),  # Delete a student

    # **Modules CRUD**
    path('api/modules/', views.module_list, name='get_modules'),  # Fetch all modules
    path('api/modules/create/', views.create_module, name='create_module'),  # Create a new module
    path('api/modules/<int:module_id>/', views.module_detail, name='module_detail'),  # Get module details
    path('api/modules/<int:module_id>/update/', views.update_module, name='update_module'),  # Update a module
    path('api/modules/<int:module_id>/delete/', views.delete_module, name='delete_module'),  # Delete a module

    # **Enrollments CRUD**
    path('api/enrollments/', views.get_enrollments, name='get_enrollments'),  # Fetch all enrollments
    path('api/enrollments/create/', views.create_enrollment, name='create_enrollment'),  # Create an enrollment
    path('api/enrollments/<int:student_id>/<int:module_id>/unenroll/', views.unenroll, name='unenroll'),  # Unenroll a student from a module

    # **Existing Views (Enrollment related)**
    path('api/students/<int:student_id>/modules/<int:module_id>/update/', views.update_enrollment, name='update_enrollment'),  # Update enrollment (e.g., grade) for a student in a specific module
]
