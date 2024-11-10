import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import Student, Module, Enrollment

# Utility function to return error for not found objects
def handle_object_not_found(model, object_id, object_name):
    try:
        return model.objects.get(id=object_id)
    except model.DoesNotExist:
        return JsonResponse({'error': f'{object_name} not found'}, status=404)

# --- Student Views ---

@require_http_methods(["GET"])
def student_list(request):
    """Retrieve all students."""
    students = list(Student.objects.all().values('id', 'first_name', 'last_name', 'email', 'date_of_birth', 'year_group'))
    return JsonResponse(students, safe=False)

@require_http_methods(["GET"])
def student_detail(request, student_id):
    """Retrieve a single student by ID."""
    student = handle_object_not_found(Student, student_id, 'Student')
    if isinstance(student, JsonResponse):
        return student
    return JsonResponse({
        'id': student.id,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'email': student.email,
        'date_of_birth': student.date_of_birth.isoformat(),
        'year_group': student.year_group
    })

@csrf_exempt
@require_http_methods(["POST"])
def create_student(request):
    """Create a new student."""
    try:
        data = json.loads(request.body)
        required_fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'year_group', 'student_id']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return JsonResponse({'error': f'Missing fields: {", ".join(missing_fields)}'}, status=400)

        student = Student.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            date_of_birth=data['date_of_birth'],
            year_group=data['year_group'],
            student_id=data['student_id']
        )
        return JsonResponse({'message': 'Student created successfully', 'id': student.id}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["PUT"])
def update_student(request, student_id):
    """Update a student record."""
    try:
        data = json.loads(request.body)
        student = Student.objects.get(id=student_id)

        student.first_name = data.get('first_name', student.first_name)
        student.last_name = data.get('last_name', student.last_name)
        student.email = data.get('email', student.email)
        student.date_of_birth = data.get('date_of_birth', student.date_of_birth)
        student.year_group = data.get('year_group', student.year_group)
        student.student_id = data.get('student_id', student.student_id)  # Update student_id
        student.save()

        return JsonResponse({'message': 'Student updated successfully'})
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_student(request, student_id):
    """Delete a student."""
    student = handle_object_not_found(Student, student_id, 'Student')
    if isinstance(student, JsonResponse):
        return student
    student.delete()
    return JsonResponse({'message': 'Student deleted successfully'})

# --- Module Views ---

@require_http_methods(["GET"])
def module_list(request):
    """Retrieve all modules."""
    modules = list(Module.objects.all().values('id', 'name', 'description', 'module_code'))
    return JsonResponse(modules, safe=False)

@require_http_methods(["GET"])
def module_detail(request, module_id):
    """Retrieve a single module by ID."""
    module = handle_object_not_found(Module, module_id, 'Module')
    if isinstance(module, JsonResponse):
        return module
    return JsonResponse({
        'id': module.id,
        'name': module.name,
        'description': module.description,
        'module_code': module.module_code
    })

@csrf_exempt
@require_http_methods(["POST"])
def create_module(request):
    """Create a new module."""
    data = json.loads(request.body)
    module = Module.objects.create(
        name=data['name'],
        description=data['description'],
        module_code=data['module_code']
    )
    return JsonResponse({'message': 'Module created', 'id': module.id}, status=201)

@csrf_exempt
@require_http_methods(["PUT"])
def update_module(request, module_id):
    """Update an existing module."""
    data = json.loads(request.body)
    module = handle_object_not_found(Module, module_id, 'Module')
    if isinstance(module, JsonResponse):
        return module
    module.name = data.get('name', module.name)
    module.description = data.get('description', module.description)
    module.module_code = data.get('module_code', module.module_code)
    module.save()
    return JsonResponse({'message': 'Module updated successfully'})

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_module(request, module_id):
    """Delete a module."""
    module = handle_object_not_found(Module, module_id, 'Module')
    if isinstance(module, JsonResponse):
        return module
    module.delete()
    return JsonResponse({'message': 'Module deleted successfully'})

# --- Enrollment Views ---

@require_http_methods(["GET"])
def enrollment_list(request):
    """Retrieve all enrollments."""
    enrollments = Enrollment.objects.all().select_related('student', 'module')
    enrollment_data = [
        {
            'id': enrollment.id,
            'student_id': enrollment.student.id,
            'student_name': f"{enrollment.student.first_name} {enrollment.student.last_name}",
            'module_id': enrollment.module.id,
            'module_name': enrollment.module.name,
            'grade': enrollment.grade,
            'date_enrolled': enrollment.date_enrolled.isoformat()
        }
        for enrollment in enrollments
    ]
    return JsonResponse(enrollment_data, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def create_enrollment(request):
    """Create a new enrollment."""
    data = json.loads(request.body)
    student = handle_object_not_found(Student, data['student_id'], 'Student')
    if isinstance(student, JsonResponse):
        return student
    module = handle_object_not_found(Module, data['module_id'], 'Module')
    if isinstance(module, JsonResponse):
        return module
    enrollment = Enrollment.objects.create(
        student=student,
        module=module,
        grade=data.get('grade')
    )
    return JsonResponse({'message': 'Enrollment created', 'id': enrollment.id}, status=201)

@csrf_exempt
@require_http_methods(["PUT"])
def update_enrollment(request, enrollment_id):
    """Update an enrollment."""
    data = json.loads(request.body)
    enrollment = handle_object_not_found(Enrollment, enrollment_id, 'Enrollment')
    if isinstance(enrollment, JsonResponse):
        return enrollment
    enrollment.grade = data.get('grade', enrollment.grade)
    enrollment.save()
    return JsonResponse({'message': 'Enrollment updated successfully'})

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_enrollment(request, enrollment_id):
    """Delete an enrollment."""
    enrollment = handle_object_not_found(Enrollment, enrollment_id, 'Enrollment')
    if isinstance(enrollment, JsonResponse):
        return enrollment
    enrollment.delete()
    return JsonResponse({'message': 'Enrollment deleted successfully'})
