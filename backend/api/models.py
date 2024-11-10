from django.db import models
from datetime import date

class Student(models.Model):
    student_id = models.CharField(max_length=9, primary_key=True)  # New field
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    date_of_birth = models.DateField()
    year_group = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

class Module(models.Model):
    name = models.CharField(max_length=100)
    module_code = models.CharField(max_length=20, unique=True)  # New field for module code
    description = models.TextField()
    
    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey(Student, to_field='student_id', on_delete=models.CASCADE)    
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)  # Use date.today for default
    grade = models.IntegerField(null=True, blank=True)  # Extra field in the through model

    class Meta:
        unique_together = ('student', 'module')

    def __str__(self):
        return f"{self.student} - {self.module}"
