# Generated by Django 5.0.1 on 2024-11-10 11:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0005_alter_enrollment_unique_together_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="module",
            name="module_code",
            field=models.CharField(default="ECS4414U", max_length=20, unique=True),
            preserve_default=False,
        ),
    ]