import { createApp } from 'vue'
import App from './App.vue'

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";

createApp(App).mount('#app');

createStudent(); {
    fetch('/api/students/create/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(this.newStudent)
    })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json(); // Parse the response as JSON
      })
      .then(data => {
        if (data.student) {
          // Add the newly created student to the list
          this.students.push(data.student);
          // Reset the form
          this.newStudent = { first_name: '', last_name: '', email: '', date_of_birth: '' };
          alert('Student added successfully');
        } else {
          throw new Error("Unexpected response: Missing student data.");
        }
      })
      .catch(error => {
        alert('Error adding student: ' + error.message);
      });
  }
  