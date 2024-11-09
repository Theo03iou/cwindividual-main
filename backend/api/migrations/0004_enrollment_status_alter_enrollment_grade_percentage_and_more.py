# Generated by Django 5.0.1 on 2024-11-09 22:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0003_rename_name_student_first_name_student_last_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="enrollment",
            name="status",
            field=models.CharField(
                choices=[
                    ("active", "Active"),
                    ("completed", "Completed"),
                    ("dropped", "Dropped"),
                ],
                default="active",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="enrollment",
            name="grade_percentage",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=5, null=True
            ),
        ),
        migrations.AlterField(
            model_name="student",
            name="year_group",
            field=models.IntegerField(),
        ),
    ]