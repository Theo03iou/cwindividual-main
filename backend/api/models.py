from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True)
    year_group = models.CharField(max_length=1)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

class Module(models.Model):
    title = models.CharField(max_length=128)
    module_code = models.CharField(max_length=8)
    description = models.TextField()
    students = models.ManyToManyField(Student, through='Enrollment', related_name='lessons')
    currently_enrolled = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    grade_percentage = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} enrolled in {self.module.title}"
