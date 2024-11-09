from django.contrib import admin
from .models import Student, Module, Enrollment

# Inline for Enrollments
class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1
    raw_id_fields = ('student', 'module')

# Admin for Student
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'date_of_birth', 'year_group')
    list_filter = ('year_group', 'date_of_birth')
    search_fields = ('first_name', 'last_name', 'email')
    inlines = [EnrollmentInline]

# Admin for Module
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'module_code', 'currently_enrolled')
    list_filter = ('currently_enrolled',)
    search_fields = ('title', 'module_code', 'description')
    inlines = [EnrollmentInline]