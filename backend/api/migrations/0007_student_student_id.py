from django.db import migrations, models
import uuid

def set_unique_student_ids(apps, schema_editor):
    Student = apps.get_model('api', 'Student')
    for student in Student.objects.all():
        student.student_id = str(uuid.uuid4())[:8]  # Assign a unique 8-character ID
        student.save()

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_module_module_code'),  # Update to your last migration
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='student_id',
            field=models.CharField(max_length=10, unique=True, null=True),  # Allow NULL temporarily
        ),
        migrations.RunPython(set_unique_student_ids),  # Assign unique student_id
        migrations.AlterField(
            model_name='student',
            name='student_id',
            field=models.CharField(max_length=10, unique=True),  # Make it non-nullable
        ),
    ]
