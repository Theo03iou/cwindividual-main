import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Student, Module, Enrollment


# GET: List available modules
@require_http_methods(["GET"])
def get_modules(request):
    modules = Module.objects.all().values('id', 'title', 'module_code', 'description')
    return JsonResponse(list(modules), safe=False)


# POST: Enroll a student in a module
@csrf_exempt
@require_http_methods(["POST"])
def enroll_in_module(request, student_id):
    data = json.loads(request.body)
    module_id = data.get('module_id')
    grade_percentage = data.get('grade_percentage', None)  # Optional

    try:
        student = Student.objects.get(id=student_id)
        module = Module.objects.get(id=module_id)

        # Check if student is already enrolled in this module
        if Enrollment.objects.filter(student=student, module=module).exists():
            return JsonResponse({'error': 'Student is already enrolled in this module'}, status=400)

        # Enroll the student in the module
        enrollment = Enrollment(student=student, module=module, grade_percentage=grade_percentage)
        enrollment.save()

        return JsonResponse({'message': 'Successfully enrolled in the module'})

    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Module.DoesNotExist:
        return JsonResponse({'error': 'Module not found'}, status=404)


# PUT: Update enrollment (e.g., grade)
@csrf_exempt
@require_http_methods(["PUT"])
def update_enrollment(request, student_id, module_id):
    data = json.loads(request.body)
    grade_percentage = data.get('grade_percentage', None)  # Optional

    try:
        student = Student.objects.get(id=student_id)
        module = Module.objects.get(id=module_id)

        # Check if the student is enrolled in the module
        enrollment = Enrollment.objects.get(student=student, module=module)

        # Update the grade percentage if provided
        if grade_percentage:
            enrollment.grade_percentage = grade_percentage
            enrollment.save()

        return JsonResponse({'message': 'Enrollment updated successfully'})

    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Module.DoesNotExist:
        return JsonResponse({'error': 'Module not found'}, status=404)
    except Enrollment.DoesNotExist:
        return JsonResponse({'error': 'Enrollment not found'}, status=400)


# DELETE: Unenroll a student from a module
@csrf_exempt
@require_http_methods(["DELETE"])
def unenroll_from_module(request, student_id, module_id):
    try:
        student = Student.objects.get(id=student_id)
        module = Module.objects.get(id=module_id)

        # Check if the student is enrolled in the module
        enrollment = Enrollment.objects.get(student=student, module=module)

        # Delete the enrollment
        enrollment.delete()

        return JsonResponse({'message': 'Successfully unenrolled from the module'})

    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Module.DoesNotExist:
        return JsonResponse({'error': 'Module not found'}, status=404)
    except Enrollment.DoesNotExist:
        return JsonResponse({'error': 'Student is not enrolled in this module'}, status=400)
