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
          <li
            class="list-group-item d-flex justify-content-between align-items-center"
            v-for="student in students"
            :key="student.student_id"
          >
            {{ student.first_name }} {{ student.last_name }}
            <div>
              <button class="btn btn-warning btn-sm" @click="editEntry('student', student)">Edit</button>
              <button class="btn btn-danger btn-sm ms-2" @click="deleteEntry('student', student.student_id)">Delete</button>
            </div>
          </li>
        </ul>
      </div>

      <!-- Modules Tab -->
      <div class="tab-pane fade" id="modules" role="tabpanel">
        <h2>Modules</h2>
        <button class="btn btn-primary mb-3" @click="showModal('module')">Add Module</button>
        <ul class="list-group">
          <li
            class="list-group-item d-flex justify-content-between align-items-center"
            v-for="module in modules"
            :key="module.id"
          >
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
          <li
            class="list-group-item d-flex justify-content-between align-items-center"
            v-for="enrollment in enrollments"
            :key="enrollment.id"
          >
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
          <div v-for="(value, key) in form" :key="`enrollment-${key}`" class="mb-3" v-if="currentEntity === 'enrollment'">
            <label :for="key" class="form-label">{{ formatLabel(key) }}</label>
            
            <select v-if="key === 'student_id'" v-model="form.student_id" id="key" class="form-control" required>
              <option value="" disabled>Select a student</option>
              <option v-for="student in students" :key="`student-${student.student_id}`" :value="student.student_id">
                {{ student.first_name }} {{ student.last_name }}
              </option>
            </select>

            <select v-else-if="key === 'module_id'" v-model="form.module_id" id="key" class="form-control" required>
              <option value="" disabled>Select a module</option>
              <option v-for="module in modules" :key="`module-${module.id}`" :value="module.id">
                {{ module.module_code }} - {{ module.name }}
              </option>
            </select>

            <input v-else v-model="form[key]" :id="key" :type="getInputType(key)" class="form-control" required />
          </div>

          <div v-else v-for="(value, key) in form" :key="`form-${key}`" class="mb-3">
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
import { Modal } from 'bootstrap';

export default {
  data() {
    return {
      students: [],
      modules: [],
      enrollments: [],
      form: {},
      isEditing: false,
      currentEntity: '',
      modalTitle: '',
      currentId: null,
    };
  },
  methods: {
    async fetchData(entity) {
      try {
        const response = await fetch(`/api/${entity}s/`);
        if (!response.ok) {
          throw new Error(`Failed to fetch ${entity}s`);
        }
        this[entity + 's'] = await response.json();
      } catch (error) {
        console.error(`Failed to fetch ${entity}s:`, error);
      }
    },
    showModal(entity) {
      this.resetForm(entity);
      this.modalTitle = this.capitalize(entity);
      this.isEditing = false;

      const modal = Modal.getOrCreateInstance(document.getElementById('entryModal'));
      modal.show();
    },
    editEntry(entity, entry) {
      this.form = { ...entry };
      this.currentId = entry.student_id || entry.id; // Handles both students and modules
      this.currentEntity = entity;
      this.modalTitle = `Edit ${this.capitalize(entity)}`;
      this.isEditing = true;

      const modal = Modal.getOrCreateInstance(document.getElementById('entryModal'));
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
        this.fetchData(this.currentEntity); // Refresh list
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
        this.fetchData(this.currentEntity); // Refresh list
        Modal.getInstance(document.getElementById('entryModal')).hide();
      } catch (error) {
        console.error(`Failed to update ${this.currentEntity}:`, error);
      }
    },
    async deleteEntry(entity, id) {
      try {
        const response = await fetch(`/api/${entity}s/${id}/delete/`, { method: 'DELETE' });
        if (!response.ok) throw new Error(`Failed to delete ${entity}`);
        this.fetchData(entity); // Refresh the list after deletion
      } catch (error) {
        console.error(`Failed to delete ${entity}:`, error);
      }
    },
    resetForm(entity) {
      this.currentEntity = entity;
      this.form = {};
      if (entity === 'student') {
        this.form = {
          student_id: '',
          first_name: '',
          last_name: '',
          email: '',
          date_of_birth: '',
          year_group: '',
        };
      } else if (entity === 'module') {
        this.form = {
          module_code: '',
          name: '',
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
    this.fetchData('student');
    this.fetchData('module');
    this.fetchData('enrollment');
  },
};
</script>

<style scoped>
.container {
  max-width: 900px;
}
</style>
