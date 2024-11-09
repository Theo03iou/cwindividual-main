<template>
    <div class="container">
      <!-- List of Students -->
      <div class="row mt-4">
        <div class="col-12">
          <h3>Student List</h3>
          <div v-for="student in students" :key="student.id" class="d-flex justify-content-between align-items-center mb-3">
            <span>{{ student.first_name }} {{ student.last_name }}</span>
            <button class="btn btn-danger" @click="deleteStudent(student.id)">Delete</button>
            <button class="btn btn-primary" @click="editStudent(student)">Edit</button>
          </div>
        </div>
      </div>
    
      <!-- Add New Student Form -->
      <div class="row mt-4">
        <div class="col-12">
          <h3>Add New Student</h3>
          <form @submit.prevent="createStudent">
            <div class="mb-3">
              <input v-model="newStudent.first_name" class="form-control" placeholder="First Name" required />
            </div>
            <div class="mb-3">
              <input v-model="newStudent.last_name" class="form-control" placeholder="Last Name" required />
            </div>
            <div class="mb-3">
              <input v-model="newStudent.email" type="email" class="form-control" placeholder="Email" required />
            </div>
            <div class="mb-3">
              <input v-model="newStudent.date_of_birth" type="date" class="form-control" required />
            </div>
            <button class="btn btn-success" type="submit">Add Student</button>
          </form>
        </div>
      </div>
    
      <!-- Edit Student Modal -->
      <div v-if="editingStudent" class="modal" tabindex="-1" role="dialog" id="editStudentModal">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Edit Student</h5>
              <button type="button" class="close" @click="closeEditModal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="updateStudent">
                <div class="mb-3">
                  <input v-model="editStudent.first_name" class="form-control" placeholder="First Name" required />
                </div>
                <div class="mb-3">
                  <input v-model="editStudent.last_name" class="form-control" placeholder="Last Name" required />
                </div>
                <div class="mb-3">
                  <input v-model="editStudent.email" type="email" class="form-control" placeholder="Email" required />
                </div>
                <div class="mb-3">
                  <input v-model="editStudent.date_of_birth" type="date" class="form-control" required />
                </div>
                <button class="btn btn-primary" type="submit">Update Student</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        students: [],  // List of students
        newStudent: {  // Data for a new student
          first_name: '',
          last_name: '',
          email: '',
          date_of_birth: ''
        },
        editStudent: null,  // Student currently being edited
        editingStudent: false, // Flag to control the modal visibility
      };
    },
    methods: {
      fetchStudents() {
        fetch('/api/students/')
          .then(response => response.json())
          .then(data => {
            this.students = data;
          })
          .catch(error => {
            alert('Error fetching students: ' + error.message);
          });
      },
      createStudent() {
        if (this.newStudent.first_name && this.newStudent.last_name && this.newStudent.email && this.newStudent.date_of_birth) {
          fetch('/api/students/create/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.newStudent)
          })
            .then(response => response.json())
            .then(data => {
              this.students.push(data);
              this.newStudent = { first_name: '', last_name: '', email: '', date_of_birth: '' }; // Reset form
              alert('Student added successfully');
            })
            .catch(error => {
              alert('Error adding student: ' + error.message);
            });
        } else {
          alert('Please fill all fields.');
        }
      },
      deleteStudent(id) {
        if (confirm('Are you sure you want to delete this student?')) {
          fetch(`/api/students/${id}/delete/`, {
            method: 'DELETE'
          })
            .then(() => {
              this.students = this.students.filter(student => student.id !== id);
              alert('Student deleted');
            })
            .catch(error => {
              alert('Error deleting student: ' + error.message);
            });
        }
      },
      editStudent(student) {
        this.editStudent = { ...student }; // Copy the student data for editing
        this.editingStudent = true;
      },
      updateStudent() {
        fetch(`/api/students/${this.editStudent.id}/update/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.editStudent)
        })
          .then(response => response.json())
          .then(data => {
            const index = this.students.findIndex(student => student.id === this.editStudent.id);
            this.students.splice(index, 1, data); // Update student in list
            this.closeEditModal();
            alert('Student updated');
          })
          .catch(error => {
            alert('Error updating student: ' + error.message);
          });
      },
      closeEditModal() {
        this.editingStudent = false;
        this.editStudent = null;
      }
    },
    mounted() {
      this.fetchStudents();
    }
  };
  </script>
  
  <style scoped>
  /* Add custom styling here if needed */
  </style>
  