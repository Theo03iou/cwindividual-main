from django.contrib import admin
from .models import Student, Module, Enrollment

# Inline for Enrollments
class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1  # Number of empty forms to show
    raw_id_fields = ('student', 'module')  # Use raw id fields for foreign key selections (optional)

# Admin for Student
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'date_of_birth', 'year_group')  # Customize based on your fields
    list_filter = ('year_group', 'date_of_birth')  # Filter by year_group and date_of_birth
    search_fields = ('first_name', 'last_name', 'email')  # Search by first name, last name, and email
    inlines = [EnrollmentInline]  # Add inline for Enrollment to show Enrollments under Student

# Admin for Module
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'module_code', 'currently_enrolled')  # Customize based on your fields
    list_filter = ('currently_enrolled',)  # Filter by currently_enrolled status
    search_fields = ('title', 'module_code', 'description')  # Search by title, module code, or description
    inlines = [EnrollmentInline]  # Add inline for Enrollment to show Enrollments under Module

# Admin for Enrollment
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'module', 'grade_percentage')  # Customize based on your fields
    list_filter = ('grade_percentage',)  # Filter by grade_percentage
    search_fields = ('student__first_name', 'student__last_name', 'module__title')  # Search by student first/last name or module title
