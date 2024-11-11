<template>
    <div>
      <h2>Enrollments</h2>
      <button class="btn btn-primary mb-3" @click="showModal">Add Enrollment</button>
      <ul class="list-group">
        <li
          class="list-group-item d-flex justify-content-between align-items-center"
          v-for="enrollment in enrollments"
          :key="enrollment.id"
        >
          {{ enrollment.student_name }} enrolled in {{ enrollment.module_name }}
          <div>
            <button class="btn btn-danger btn-sm ms-2" @click="deleteEnrollment(enrollment.id)">Delete</button>
          </div>
        </li>
      </ul>
  
      <!-- Modal for Adding Enrollment -->
      <div class="modal fade" tabindex="-1" id="enrollmentModal">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Add Enrollment</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="addEnrollment">
                <div class="mb-3">
                  <label for="student_id" class="form-label">Student</label>
                  <select v-model="form.student_id" id="student_id" class="form-control" required>
                    <option value="" disabled>Select a student</option>
                    <option v-for="student in students" :key="student.student_id" :value="student.student_id">
                      {{ student.first_name }} {{ student.last_name }}
                    </option>
                  </select>
                </div>
                <div class="mb-3">
                  <label for="module_id" class="form-label">Module</label>
                  <select v-model="form.module_id" id="module_id" class="form-control" required>
                    <option value="" disabled>Select a module</option>
                    <option v-for="module in modules" :key="module.id" :value="module.id">
                      {{ module.module_code }} - {{ module.name }}
                    </option>
                  </select>
                </div>
                <button type="submit" class="btn btn-success">Add</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { Modal } from 'bootstrap';
  
  export default {
    props: ['students', 'modules'],
    data() {
      return {
        enrollments: [],
        form: {
          student_id: '',
          module_id: '',
        },
      };
    },
    methods: {
      async fetchEnrollments() {
        try {
          const response = await fetch('/api/enrollments/');
          if (!response.ok) throw new Error('Failed to fetch enrollments');
          this.enrollments = await response.json();
        } catch (error) {
          console.error('Error fetching enrollments:', error);
        }
      },
      showModal() {
        this.resetForm();
        const modal = Modal.getOrCreateInstance(document.getElementById('enrollmentModal'));
        modal.show();
      },
      resetForm() {
        this.form = {
          student_id: '',
          module_id: '',
        };
      },
      async addEnrollment() {
        try {
          const response = await fetch('/api/enrollments/create/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(this.form),
          });
          if (!response.ok) throw new Error('Failed to add enrollment');
          this.fetchEnrollments();
          Modal.getInstance(document.getElementById('enrollmentModal')).hide();
        } catch (error) {
          console.error('Error adding enrollment:', error);
        }
      },
      async deleteEnrollment(id) {
        try {
          const response = await fetch(`/api/enrollments/${id}/delete/`, { method: 'DELETE' });
          if (!response.ok) throw new Error('Failed to delete enrollment');
          this.fetchEnrollments();
        } catch (error) {
          console.error('Error deleting enrollment:', error);
        }
      },
    },
    mounted() {
      this.fetchEnrollments();
    },
  };
  </script>
  
  <style scoped>
  /* Optional: Add component-specific styles here */
  </style>