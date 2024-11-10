from django.contrib import admin
from .models import Student, Module, Enrollment

# Inline for Enrollment, to be used within Student and Module Admin pages
class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1
    fields = ('module', 'grade', 'date_enrolled')
    readonly_fields = ('date_enrolled',)
    raw_id_fields = ('module',)  # To make selection easier in the dropdown

# Admin for Student
@admin.register(Student)  # Ensure Student is registered
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'email', 'date_of_birth', 'year_group')
    list_filter = ('year_group', 'date_of_birth')
    search_fields = ('student_id', 'first_name', 'last_name', 'email')
    inlines = [EnrollmentInline]

# Admin for Module
@admin.register(Module)  # Ensure Module is registered
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'module_code', 'description')
    search_fields = ('name', 'module_code')
    inlines = [EnrollmentInline]

# # Admin for Enrollment (optional, for standalone management if needed)
# @admin.register(Enrollment)
# class EnrollmentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'student', 'module', 'grade', 'date_enrolled')
#     list_filter = ('date_enrolled', 'grade')
#     search_fields = ('student__first_name', 'student__last_name', 'module__name')
#     raw_id_fields = ('student', 'module')  # Optimizes foreign key dropdowns for large datasets
