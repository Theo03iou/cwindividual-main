from django.contrib import admin
from .models import Student, Module, Enrollment

class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1
    fields = ('module', 'date_enrolled')
    readonly_fields = ('date_enrolled',)
    raw_id_fields = ('module',)  
    
@admin.register(Student)  
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'email', 'date_of_birth', 'year_group')
    list_filter = ('year_group', 'date_of_birth')
    search_fields = ('student_id', 'first_name', 'last_name', 'email')
    inlines = [EnrollmentInline]

@admin.register(Module)  
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'module_code', 'description')
    search_fields = ('name', 'module_code')
    inlines = [EnrollmentInline]
