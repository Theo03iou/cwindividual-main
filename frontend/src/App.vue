<template>
  <div class="container mt-4">
    <h1 class="text-center">University Management System</h1>

    <!-- Bootstrap Tabs -->
    <ul class="nav nav-tabs" role="tablist">
      <li class="nav-item">
        <a class="nav-link active" data-bs-toggle="tab" href="#students" role="tab">Students</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" data-bs-toggle="tab" href="#modules" role="tab">Modules</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" data-bs-toggle="tab" href="#enrollments" role="tab">Enrollments</a>
      </li>
    </ul>

    <div class="tab-content mt-3">
      <!-- Students Tab -->
      <div class="tab-pane fade show active" id="students" role="tabpanel">
        <h2>Students</h2>
        <button class="btn btn-primary mb-3" @click="showModal('student')">Add Student</button>
        <ul class="list-group">
          <li class="list-group-item d-flex justify-content-between align-items-center" v-for="student in students" :key="student.id">
            {{ student.student_id }} - {{ student.first_name }} {{ student.last_name }}
            <div>
              <button class="btn btn-warning btn-sm" @click="editEntry('student', student)">Edit</button>
              <button class="btn btn-danger btn-sm ms-2" @click="deleteEntry('student', student.id)">Delete</button>
            </div>
          </li>
        </ul>
      </div>

      <!-- Modules Tab -->
      <div class="tab-pane fade" id="modules" role="tabpanel">
        <h2>Modules</h2>
        <button class="btn btn-primary mb-3" @click="showModal('module')">Add Module</button>
        <ul class="list-group">
          <li class="list-group-item d-flex justify-content-between align-items-center" v-for="module in modules" :key="module.id">
            {{ module.module_code }} - {{ module.name }}
            <div>
              <button class="btn btn-warning btn-sm" @click="editEntry('module', module)">Edit</button>
              <button class="btn btn-danger btn-sm ms-2" @click="deleteEntry('module', module.id)">Delete</button>
            </div>
          </li>
        </ul>
      </div>

      <!-- Enrollments Tab -->
      <div class="tab-pane fade" id="enrollments" role="tabpanel">
        <h2>Enrollments</h2>
        <button class="btn btn-primary mb-3" @click="showModal('enrollment')">Add Enrollment</button>
        <ul class="list-group">
          <li class="list-group-item d-flex justify-content-between align-items-center" v-for="enrollment in enrollments" :key="enrollment.id">
            {{ enrollment.student_name }} enrolled in {{ enrollment.module_name }} (Grade: {{ enrollment.grade }})
            <div>
              <button class="btn btn-warning btn-sm" @click="editEntry('enrollment', enrollment)">Edit</button>
              <button class="btn btn-danger btn-sm ms-2" @click="deleteEntry('enrollment', enrollment.id)">Delete</button>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <!-- Modal for Adding and Editing -->
    <div class="modal fade" tabindex="-1" id="entryModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ isEditing ? 'Edit' : 'Add' }} {{ modalTitle }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="isEditing ? updateEntry() : addEntry()">
              <!-- Dynamic Form Inputs -->
              <div v-for="(value, key) in form" :key="key" class="mb-3">
                <label :for="key" class="form-label">{{ formatLabel(key) }}</label>
                <input v-model="form[key]" :id="key" :type="getInputType(key)" class="form-control" required />
              </div>
              <button type="submit" class="btn btn-success">{{ isEditing ? 'Update' : 'Add' }}</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from 'bootstrap'; // Import Modal directly

export default {
  data() {
    return {
      students: [],
      modules: [],
      enrollments: [],
      form: {}, // Dynamic form object
      isEditing: false,
      currentEntity: '', // 'student', 'module', or 'enrollment'
      modalTitle: '',
      currentId: null, // ID of the entry being edited
    };
  },
  methods: {
    async fetchData(entity) {
      try {
        const response = await fetch(`/api/${entity}/`);
        this[entity] = await response.json();
      } catch (error) {
        console.error(`Failed to fetch ${entity}:`, error);
      }
    },
    showModal(entity) {
      this.resetForm(entity);
      this.modalTitle = this.capitalize(entity);
      this.isEditing = false;

      const modal = new Modal(document.getElementById('entryModal'));
      modal.show();
    },
    editEntry(entity, entry) {
      this.form = { ...entry };
      this.currentId = entry.id;
      this.currentEntity = entity;
      this.modalTitle = this.capitalize(entity);
      this.isEditing = true;

      const modal = new Modal(document.getElementById('entryModal'));
      modal.show();
    },
    async addEntry() {
      try {
        const response = await fetch(`/api/${this.currentEntity}s/create/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.form),
        });
        if (!response.ok) throw new Error('Failed to add entry');
        this.fetchData(this.currentEntity + 's');
        Modal.getInstance(document.getElementById('entryModal')).hide();
      } catch (error) {
        console.error(`Failed to add ${this.currentEntity}:`, error);
      }
    },
    async updateEntry() {
      try {
        const response = await fetch(`/api/${this.currentEntity}s/${this.currentId}/update/`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.form),
        });
        if (!response.ok) throw new Error('Failed to update entry');
        this.fetchData(this.currentEntity + 's');
        Modal.getInstance(document.getElementById('entryModal')).hide();
      } catch (error) {
        console.error(`Failed to update ${this.currentEntity}:`, error);
      }
    },
    async deleteEntry(entity, id) {
  try {
    const response = await fetch(`/api/${entity}s/${id}/delete/`, { // Ensure proper endpoint URL
      method: 'DELETE',
    });
    if (!response.ok) throw new Error('Failed to delete entry');
    this.fetchData(entity + 's'); // Ensure correct plural entity fetching
  } catch (error) {
    console.error(`Failed to delete ${entity}:`, error);
  }
}
,
    resetForm(entity) {
      this.currentEntity = entity;
      if (entity === 'student') {
        this.form = {
          student_id: '', // New field for Student ID
          first_name: '',
          last_name: '',
          email: '',
          date_of_birth: '',
          year_group: '',
        };
      } else if (entity === 'module') {
        this.form = {
          name: '',
          module_code: '',
          description: '',
        };
      } else if (entity === 'enrollment') {
        this.form = {
          student_id: '',
          module_id: '',
          grade: '',
        };
      }
    },
    capitalize(str) {
      return str.charAt(0).toUpperCase() + str.slice(1);
    },
    formatLabel(key) {
      return key.replace(/_/g, ' ').toUpperCase();
    },
    getInputType(key) {
      return key.includes('date') ? 'date' : key.includes('email') ? 'email' : 'text';
    },
  },
  mounted() {
    this.fetchData('students');
    this.fetchData('modules');
    this.fetchData('enrollments');
  },
};
</script>

<style scoped>
.container {
  max-width: 900px;
}
</style>
