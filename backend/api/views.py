import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Student, Module, Enrollment
from django.core.exceptions import ValidationError

# FOR NOT FOUND OBJECTS
def handle_object_not_found(model, lookup_value, object_name, lookup_field='id'):
    try:
        return model.objects.get(**{lookup_field: lookup_value})
    except model.DoesNotExist:
        return JsonResponse({'error': f'{object_name} not found'}, status=404)


# STUDENT VIEWS
@require_http_methods(["GET"])
def student_list(request):
    """Retrieve all students."""
    students = list(Student.objects.all().values(
        'student_id', 'first_name', 'last_name', 'email', 'date_of_birth', 'year_group'
    ))
    return JsonResponse(students, safe=False)

@require_http_methods(["GET"])
def student_detail(request, student_id):
    """Retrieve a single student by student_id."""
    student = handle_object_not_found(Student, student_id, 'Student', lookup_field='student_id')
    if isinstance(student, JsonResponse):
        return student
    return JsonResponse({
        'student_id': student.student_id,
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
    data = json.loads(request.body)
    required_fields = ['student_id', 'first_name', 'last_name', 'email', 'date_of_birth', 'year_group']
    if not all(field in data for field in required_fields):
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    if len(str(data['student_id'])) != 9:
        return JsonResponse({'error': 'Student ID must be exactly 9 characters long'}, status=400)

    try:
        student = Student.objects.create(
            student_id=data['student_id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            date_of_birth=data['date_of_birth'],
            year_group=data['year_group']
        )
        return JsonResponse({'message': 'Student created successfully', 'student_id': student.student_id})
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Student ID already exists'}, status=400)

@csrf_exempt
@require_http_methods(["PUT"])
def update_student(request, student_id):
    """Update a student record."""
    data = json.loads(request.body)
    student = handle_object_not_found(Student, student_id, 'Student', lookup_field='student_id')
    if isinstance(student, JsonResponse):
        return student
    student.first_name = data.get('first_name', student.first_name)
    student.last_name = data.get('last_name', student.last_name)
    student.email = data.get('email', student.email)
    student.date_of_birth = data.get('date_of_birth', student.date_of_birth)
    student.year_group = data.get('year_group', student.year_group)
    student.save()

    return JsonResponse({'message': 'Student updated successfully'})

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_student(request, student_id):
    """Delete a student."""
    student = handle_object_not_found(Student, student_id, 'Student', lookup_field='student_id')
    if isinstance(student, JsonResponse):
        return student
    student.delete()
    return JsonResponse({'message': 'Student deleted successfully'})

# MODULE VIEWS

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

# ENROLLMENT VIEWS

@require_http_methods(["GET"])
def enrollment_list(request):
    """Retrieve all enrollments."""
    enrollments = Enrollment.objects.all().select_related('student', 'module')
    enrollment_data = [
        {
            'id': enrollment.id,
            'student_id': enrollment.student.student_id,
            'student_name': f"{enrollment.student.first_name} {enrollment.student.last_name}",
            'module_id': enrollment.module.id,
            'module_name': enrollment.module.name,
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
    student = handle_object_not_found(Student, data['student_id'], 'Student', lookup_field='student_id')
    if isinstance(student, JsonResponse):
        return student
    module = handle_object_not_found(Module, data['module_id'], 'Module')
    if isinstance(module, JsonResponse):
        return module
    enrollment = Enrollment.objects.create(
        student=student,
        module=module,
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

   
