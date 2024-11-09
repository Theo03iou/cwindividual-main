import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from .models import Student, Module, Enrollment


# Utility function to handle object not found
def handle_object_not_found(model, object_id, object_name):
    try:
        return model.objects.get(id=object_id)
    except model.DoesNotExist:
        return JsonResponse({'error': f'{object_name} not found'}, status=404)


# --- Students Views ---

@require_http_methods(["GET"])
def student_list(request):
    students = Student.objects.all().values('id', 'first_name', 'last_name', 'email', 'date_of_birth', 'year_group')
    return JsonResponse(list(students), safe=False)


@require_http_methods(["GET"])
def student_detail(request, student_id):
    student = handle_object_not_found(Student, student_id, 'Student')
    if isinstance(student, JsonResponse):  # If an error response is returned
        return student
    
    return JsonResponse({
        'id': student.id,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'email': student.email,
        'date_of_birth': student.date_of_birth,
        'year_group': student.year_group
    })


@csrf_exempt
@require_http_methods(["POST"])
def create_student(request):
    data = json.loads(request.body)
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    date_of_birth = data.get('date_of_birth')
    year_group = data.get('year_group')

    if not all([first_name, last_name, email, date_of_birth, year_group]):
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    student = Student.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        date_of_birth=date_of_birth,
        year_group=year_group
    )
    return JsonResponse({'message': 'Student created successfully', 'id': student.id})


@csrf_exempt
@require_http_methods(["PUT"])
def update_student(request, student_id):
    data = json.loads(request.body)
    student = handle_object_not_found(Student, student_id, 'Student')
    if isinstance(student, JsonResponse):  # If an error response is returned
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
    student = handle_object_not_found(Student, student_id, 'Student')
    if isinstance(student, JsonResponse):  # If an error response is returned
        return student
    
    student.delete()
    return JsonResponse({'message': 'Student deleted successfully'})


# --- Modules Views ---

@require_http_methods(["GET"])
def module_list(request):
    modules = Module.objects.all().values('id', 'title', 'module_code', 'description', 'currently_enrolled')
    return JsonResponse(list(modules), safe=False)


@require_http_methods(["GET"])
def module_detail(request, module_id):
    module = handle_object_not_found(Module, module_id, 'Module')
    if isinstance(module, JsonResponse):  # If an error response is returned
        return module
    
    return JsonResponse({
        'id': module.id,
        'title': module.title,
        'module_code': module.module_code,
        'description': module.description,
        'currently_enrolled': module.currently_enrolled
    })


@csrf_exempt
@require_http_methods(["POST"])
def create_module(request):
    data = json.loads(request.body)
    title = data.get('title')
    module_code = data.get('module_code')
    description = data.get('description')
    currently_enrolled = data.get('currently_enrolled')

    if not all([title, module_code, description]):
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    module = Module.objects.create(
        title=title,
        module_code=module_code,
        description=description,
        currently_enrolled=currently_enrolled
    )
    return JsonResponse({'message': 'Module created successfully', 'id': module.id})


@csrf_exempt
@require_http_methods(["PUT"])
def update_module(request, module_id):
    data = json.loads(request.body)
    module = handle_object_not_found(Module, module_id, 'Module')
    if isinstance(module, JsonResponse):  # If an error response is returned
        return module
    
    module.title = data.get('title', module.title)
    module.module_code = data.get('module_code', module.module_code)
    module.description = data.get('description', module.description)
    module.currently_enrolled = data.get('currently_enrolled', module.currently_enrolled)
    module.save()

    return JsonResponse({'message': 'Module updated successfully'})


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_module(request, module_id):
    module = handle_object_not_found(Module, module_id, 'Module')
    if isinstance(module, JsonResponse):  # If an error response is returned
        return module
    
    module.delete()
    return JsonResponse({'message': 'Module deleted successfully'})


# --- Enrollments Views ---

# Utility function to check duplicate enrollments
def is_duplicate_enrollment(student, module):
    return Enrollment.objects.filter(student=student, module=module).exists()


@require_http_methods(["GET"])
def get_enrollments(request):
    enrollments = Enrollment.objects.all().select_related('student', 'module')
    enrollment_data = []

    for enrollment in enrollments:
        enrollment_data.append({
            'student_id': enrollment.student.id,
            'student_name': f'{enrollment.student.first_name} {enrollment.student.last_name}',
            'module_id': enrollment.module.id,
            'module_name': enrollment.module.title,
            'grade_percentage': enrollment.grade_percentage,
        })

    return JsonResponse(enrollment_data, safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def create_enrollment(request):
    data = json.loads(request.body)
    student_id = data.get('student_id')
    module_id = data.get('module_id')
    grade_percentage = data.get('grade_percentage', None)

    student = handle_object_not_found(Student, student_id, 'Student')
    if isinstance(student, JsonResponse):  # If an error response is returned
        return student

    module = handle_object_not_found(Module, module_id, 'Module')
    if isinstance(module, JsonResponse):  # If an error response is returned
        return module

    # Check for duplicate enrollment
    if is_duplicate_enrollment(student, module):
        return JsonResponse({'error': 'Student is already enrolled in this module'}, status=400)

    # Create the enrollment
    enrollment = Enrollment.objects.create(
        student=student,
        module=module,
        grade_percentage=grade_percentage
    )

    return JsonResponse({
        'message': 'Enrollment created successfully',
        'enrollment_id': enrollment.id,
        'student': f'{student.first_name} {student.last_name}',
        'module': module.title,
        'grade_percentage': enrollment.grade_percentage,
    }, status=201)


@csrf_exempt
@require_http_methods(["PUT"])
def update_enrollment(request, student_id, module_id):
    data = json.loads(request.body)
    grade_percentage = data.get('grade_percentage', None)

    student = handle_object_not_found(Student, student_id, 'Student')
    if isinstance(student, JsonResponse):  # If an error response is returned
        return student

    module = handle_object_not_found(Module, module_id, 'Module')
    if isinstance(module, JsonResponse):  # If an error response is returned
        return module

    try:
        enrollment = Enrollment.objects.get(student=student, module=module)
    except Enrollment.DoesNotExist:
        return JsonResponse({'error': 'Enrollment not found'}, status=404)

    if grade_percentage is not None:
        enrollment.grade_percentage = grade_percentage
        enrollment.save()

    return JsonResponse({'message': 'Enrollment updated successfully'})


@csrf_exempt
@require_http_methods(["DELETE"])
def unenroll(request, student_id, module_id):
    student = handle_object_not_found(Student, student_id, 'Student')
    if isinstance(student, JsonResponse):  # If an error response is returned
        return student

    module = handle_object_not_found(Module, module_id, 'Module')
    if isinstance(module, JsonResponse):  # If an error response is returned
        return module

    try:
        enrollment = Enrollment.objects.get(student=student, module=module)
        enrollment.delete()
        return JsonResponse({'message': 'Successfully unenrolled from the module'})
    except Enrollment.DoesNotExist:
        return JsonResponse({'error': 'Student is not enrolled in this module'}, status=404)
