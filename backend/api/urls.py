from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.student_list, name='student_list'),  
    path('students/<int:student_id>/', views.student_detail, name='student_detail'),  
    path('students/create/', views.create_student, name='create_student'), 
    path('students/<int:student_id>/update/', views.update_student, name='update_student'),  
    path('students/<int:student_id>/delete/', views.delete_student, name='delete_student'),
    
    path('modules/', views.module_list, name='module_list'), 
    path('modules/<int:module_id>/', views.module_detail, name='module_detail'), 
    path('modules/create/', views.create_module, name='create_module'),  
    path('modules/<int:module_id>/update/', views.update_module, name='update_module'),  
    path('modules/<int:module_id>/delete/', views.delete_module, name='delete_module'),  
    
    path('enrollments/', views.enrollment_list, name='enrollment_list'), 
    path('enrollments/create/', views.create_enrollment, name='create_enrollment'),  
    path('enrollments/<int:enrollment_id>/update/', views.update_enrollment, name='update_enrollment'),  
    path('enrollments/<int:enrollment_id>/delete/', views.delete_enrollment, name='delete_enrollment'),  
]
