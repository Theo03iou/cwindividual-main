"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    # GET: Fetch all modules
    path('api/modules/', views.get_modules, name='get_modules'),

    # POST: Enroll a student in a module (Student ID must be provided)
    path('api/students/<int:student_id>/enroll/', views.enroll_in_module, name='enroll_in_module'),

    # PUT: Update enrollment (e.g., grade) for a student in a specific module
    path('api/students/<int:student_id>/modules/<int:module_id>/update/', views.update_enrollment, name='update_enrollment'),

    # DELETE: Unenroll a student from a module
    path('api/students/<int:student_id>/modules/<int:module_id>/unenroll/', views.unenroll_from_module, name='unenroll_from_module'),
]

