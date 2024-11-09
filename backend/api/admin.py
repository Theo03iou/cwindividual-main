from django.contrib import admin
from .models import Student, Module, Enrollment

# Inline for Enrollments
class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1  # Default number of empty forms to show
    raw_id_fields = ('student', 'module')  # Use raw id fields for foreign key selections (optional)

# Admin for Student
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'email', 'date_of_birth')  # Customize based on your fields
    list_filter = ('date_of_birth',)  # Filter by date_of_birth
    search_fields = ('last_name', 'first_name',  'email')  # Search by name and email
    inlines = [EnrollmentInline]  # Add inline for Enrollment to show Enrollments under Student

# Admin for Module
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'course', 'credits')  # Customize based on your fields
    list_filter = ('course',)  # Filter by course
    search_fields = ('last_name', 'first_name', 'course__name')  # Search by module name or associated course name
    inlines = [EnrollmentInline]  # Add inline for Enrollment to show Enrollments under Module
