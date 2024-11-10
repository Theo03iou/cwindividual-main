from django.urls import path
from . import views

urlpatterns = [
    # Student endpoints
    path('students/', views.student_list, name='student_list'),  # GET all students
    path('students/<int:student_id>/', views.student_detail, name='student_detail'),  # GET a specific student
    path('students/create/', views.create_student, name='create_student'),  # POST to create a new student
    path('students/<int:student_id>/update/', views.update_student, name='update_student'),  # PUT to update a student
    path('students/<int:student_id>/delete/', views.delete_student, name='delete_student'),  # DELETE a student
    
    # Module endpoints
    path('modules/', views.module_list, name='module_list'),  # GET all modules
    path('modules/<int:module_id>/', views.module_detail, name='module_detail'),  # GET a specific module
    path('modules/create/', views.create_module, name='create_module'),  # POST to create a new module
    path('modules/<int:module_id>/update/', views.update_module, name='update_module'),  # PUT to update a module
    path('modules/<int:module_id>/delete/', views.delete_module, name='delete_module'),  # DELETE a module
    
    # Enrollment endpoints
    path('enrollments/', views.enrollment_list, name='enrollment_list'),  # GET all enrollments
    path('enrollments/create/', views.create_enrollment, name='create_enrollment'),  # POST to create a new enrollment
    path('enrollments/<int:enrollment_id>/update/', views.update_enrollment, name='update_enrollment'),  # PUT to update an enrollment
    path('enrollments/<int:enrollment_id>/delete/', views.delete_enrollment, name='delete_enrollment'),  # DELETE an enrollment
]
