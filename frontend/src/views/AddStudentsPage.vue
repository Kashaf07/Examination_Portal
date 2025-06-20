<template>
  <div class="p-6 bg-white shadow rounded-lg max-w-xl mx-auto">
    <h2 class="text-2xl font-bold mb-4">Add Students</h2>
    <p class="mb-4 text-gray-700">
      Upload student list for Exam ID: <strong>{{ examId }}</strong>
    </p>

    <!-- File Upload -->
    <div class="mb-4">
      <label class="block mb-2 font-semibold">Upload Excel or CSV File</label>
      <input
        type="file"
        @change="handleFileUpload"
        accept=".xlsx, .csv"
        class="block w-full p-2 border rounded"
      />
    </div>

    <!-- Upload Button -->
    <button
      :disabled="!selectedFile"
      @click="uploadFile"
      class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400"
    >
      Upload Students
    </button>

    <!-- Send Notification Button -->
    <button
      @click="sendNotification"
      class="mt-4 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
    >
      Send Notification to Applicants
    </button>

    <!-- Messages -->
    <p v-if="message" class="mt-4 text-green-600">{{ message }}</p>
    <p v-if="error" class="mt-4 text-red-600">{{ error }}</p>

    <!-- Download Template -->
    <a
      href="/sample/Student_Upload_Template.csv"
      download
      class="mt-6 inline-block text-blue-600 underline"
    >
      Download Sample Excel Template
    </a>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const examId = route.params.examId

const selectedFile = ref(null)
const message = ref('')
const error = ref('')

const handleFileUpload = (e) => {
  selectedFile.value = e.target.files[0]
}

const uploadFile = async () => {
  if (!selectedFile.value) return

  const formData = new FormData()
  formData.append('file', selectedFile.value)
  formData.append('exam_id', examId)

  try {
    const response = await fetch('http://localhost:5000/api/add_students', {
      method: 'POST',
      body: formData
    })

    const result = await response.json()

    if (response.ok) {
      message.value = result.message || 'Students uploaded successfully!'
      error.value = ''
    } else {
      error.value = result.error || 'Upload failed. Please check the file format.'
      message.value = ''
    }
  } catch (err) {
    error.value = 'Server error or connection failed'
    message.value = ''
  }
}

const sendNotification = async () => {
  try {
    const response = await fetch('http://localhost:5000/api/send_exam_notification', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ exam_id: examId })
    })

    const result = await response.json()

    if (response.ok) {
      message.value = result.message || 'Notifications sent successfully!'
      error.value = ''
    } else {
      error.value = result.error || 'Failed to send notifications.'
      message.value = ''
    }
  } catch (err) {
    error.value = 'Error sending notifications.'
    message.value = ''
  }
}
</script>
