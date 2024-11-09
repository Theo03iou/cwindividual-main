

<template>
    <div class="container pt-3">
      <!-- Header -->
      <div class="h1 text-center border rounded bg-light p-2 mb-3">
        API Client
      </div>
  
      <!-- Tab Navigation -->
      <ul class="nav nav-tabs" id="myTab" role="tablist">
        <li class="nav-item" role="presentation">
          <a class="nav-link active" id="students-tab" data-bs-toggle="tab" href="#students" role="tab" aria-controls="students" aria-selected="true">Students</a>
        </li>
        <li class="nav-item" role="presentation">
          <a class="nav-link" id="modules-tab" data-bs-toggle="tab" href="#modules" role="tab" aria-controls="modules" aria-selected="false">Modules</a>
        </li>
        <li class="nav-item" role="presentation">
          <a class="nav-link" id="enrollments-tab" data-bs-toggle="tab" href="#enrollments" role="tab" aria-controls="enrollments" aria-selected="false">Enrollments</a>
        </li>
      </ul>
  
      <!-- Tab Content -->
      <div class="tab-content mt-3">
        <!-- Students Tab -->
        <div class="tab-pane fade show active" id="students" role="tabpanel" aria-labelledby="students-tab">
          <h3>Students</h3>
          <button class="btn btn-primary" @click="openStudentModal">Add Student</button>
          <ul class="list-group mt-3">
            <li v-for="student in students" :key="student.id" class="list-group-item">
              {{ student.first_name }} {{ student.last_name }}
              <button class="btn btn-warning btn-sm float-end" @click="editStudent(student)">Edit</button>
              <button class="btn btn-danger btn-sm float-end me-2" @click="deleteStudent(student.id)">Delete</button>
            </li>
          </ul>
        </div>
  
        <!-- Modules Tab -->
        <div class="tab-pane fade" id="modules" role="tabpanel" aria-labelledby="modules-tab">
          <h3>Modules</h3>
          <button class="btn btn-primary" @click="openModuleModal">Add Module</button>
          <ul class="list-group mt-3">
            <li v-for="module in modules" :key="module.id" class="list-group-item">
              {{ module.title }}
              <button class="btn btn-warning btn-sm float-end" @click="editModule(module)">Edit</button>
              <button class="btn btn-danger btn-sm float-end me-2" @click="deleteModule(module.id)">Delete</button>
            </li>
          </ul>
        </div>
  
        <!-- Enrollments Tab -->
        <div class="tab-pane fade" id="enrollments" role="tabpanel" aria-labelledby="enrollments-tab">
          <h3>Enrollments</h3>
          <button class="btn btn-primary" @click="openEnrollmentModal">Add Enrollment</button>
          <ul class="list-group mt-3">
            <li v-for="enrollment in enrollments" :key="enrollment.id" class="list-group-item">
              Student: {{ enrollment.student.first_name }} {{ enrollment.student.last_name }}
              Module: {{ enrollment.module.title }}
              <button class="btn btn-danger btn-sm float-end" @click="unenroll(enrollment.id)">Unenroll</button>
            </li>
          </ul>
        </div>
      </div>
  
      <!-- Modal for Adding/Editing Student -->
      <div class="modal fade" id="studentModal" tabindex="-1" aria-labelledby="studentModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="studentModalLabel">{{ editingStudent ? 'Edit Student' : 'Add Student' }}</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="submitStudentForm">
                <div class="mb-3">
                  <input v-model="studentForm.first_name" class="form-control" placeholder="First Name" required>
                </div>
                <div class="mb-3">
                  <input v-model="studentForm.last_name" class="form-control" placeholder="Last Name" required>
                </div>
                <div class="mb-3">
                  <input v-model="studentForm.email" class="form-control" placeholder="Email" required>
                </div>
                <div class="mb-3">
                  <input v-model="studentForm.date_of_birth" type="date" class="form-control" required>
                </div>
                <div class="mb-3">
                  <input v-model="studentForm.year_group" class="form-control" placeholder="Year Group" required>
                </div>
                <button type="submit" class="btn btn-primary">{{ editingStudent ? 'Update' : 'Create' }}</button>
              </form>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Modal for Adding/Editing Module (similar structure to student modal) -->
  
      <!-- Modal for Adding/Editing Enrollment (similar structure to student modal) -->
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        students: [],
        modules: [],
        enrollments: [],
        studentForm: {
          first_name: '',
          last_name: '',
          email: '',
          date_of_birth: '',
          year_group: ''
        },
        editingStudent: false,
        studentIdToEdit: null,
        // Similar form data for modules and enrollments
      }
    },
    async mounted() {
      await this.fetchStudents();
      await this.fetchModules();
      await this.fetchEnrollments();
    },
    methods: {
      // Fetch data for Students, Modules, Enrollments
      async fetchStudents() {
        const response = await fetch('/students/');
        this.students = await response.json();
      },
      async fetchModules() {
        const response = await fetch('/modules/');
        this.modules = await response.json();
      },
      async fetchEnrollments() {
        const response = await fetch('/enrollments/');
        this.enrollments = await response.json();
      },
  
      // Student CRUD Methods
      openStudentModal() {
        this.editingStudent = false;
        this.studentForm = { first_name: '', last_name: '', email: '', date_of_birth: '', year_group: '' };
        new bootstrap.Modal(document.getElementById('studentModal')).show();
      },
      async submitStudentForm() {
        if (this.editingStudent) {
          // PUT request to update student
          await fetch(`/students/${this.studentIdToEdit}/update/`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(this.studentForm)
          });
        } else {
          // POST request to create student
          await fetch('/students/create/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(this.studentForm)
          });
        }
        this.fetchStudents();
        this.closeModals();
      },
      async editStudent(student) {
        this.editingStudent = true;
        this.studentForm = { ...student };
        this.studentIdToEdit = student.id;
        new bootstrap.Modal(document.getElementById('studentModal')).show();
      },
      async deleteStudent(id) {
        await fetch(`/students/${id}/delete/`, { method: 'DELETE' });
        this.fetchStudents();
      },
  
      // Similar methods for Modules and Enrollments (add, edit, delete)
      // Make sure to define methods for modules and enrollments CRUD like the student methods above.
  
      closeModals() {
        const modal = new bootstrap.Modal(document.getElementById('studentModal'));
        modal.hide();
      }
    }
  }
  </script>
  
  <style scoped>
  /* Add custom styling here if needed */
  </style>
  