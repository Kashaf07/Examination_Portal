<template>
  <div class="space-y-4 bg-white p-4 shadow rounded">
    <h2 class="text-xl font-semibold mb-2">Create Exam</h2>

    <form @submit.prevent="submitExam" class="space-y-4">
      <div>
        <label class="block font-semibold">Exam Name</label>
        <input v-model="exam.exam_name" type="text" class="w-full p-2 border rounded" required />
      </div>

      <div>
        <label class="block font-semibold">Exam Date</label>
        <input v-model="exam.exam_date" type="date" class="w-full p-2 border rounded" required />
      </div>

      <div>
        <label class="block font-semibold">Exam Time</label>
        <input v-model="exam.exam_time" type="time" class="w-full p-2 border rounded" required />
      </div>

      <div>
        <label class="block font-semibold">Duration (Minutes)</label>
        <input v-model="exam.duration" type="number" class="w-full p-2 border rounded" required />
      </div>

      <div>
        <label class="block font-semibold">Total Questions</label>
        <input v-model="exam.total_questions" type="number" class="w-full p-2 border rounded" required />
      </div>

      <div>
        <label class="block font-semibold">Max Marks</label>
        <input v-model="exam.max_marks" type="number" class="w-full p-2 border rounded" required />
      </div>

      <div v-if="message" :class="success ? 'text-green-600' : 'text-red-600'" class="font-semibold">
        {{ message }}
      </div>

      <div class="flex gap-4">
        <button type="submit" class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
          Submit Exam
        </button>
        <button @click="$emit('closeForm')" type="button" class="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500">
          Cancel
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const exam = ref({
  exam_name: '',
  exam_date: '',
  exam_time: '',
  duration: '',
  total_questions: '',
  max_marks: '',
  faculty_email: localStorage.getItem('faculty_email') || ''
})

const message = ref('')
const success = ref(false)

const submitExam = async () => {
  try {
    const res = await axios.post('http://localhost:5000/api/exam/create', exam.value)
    if (res.data.success) {
      success.value = true
      message.value = `✅ Exam created successfully! Exam ID: ${res.data.exam_id}`
      // Reset form fields
      exam.value = {
        exam_name: '',
        exam_date: '',
        exam_time: '',
        duration: '',
        total_questions: '',
        max_marks: '',
        faculty_email: localStorage.getItem('faculty_email') || ''
      }
    } else {
      success.value = false
      message.value = res.data.message || 'Failed to create exam'
    }
  } catch (err) {
    success.value = false
    message.value = err.response?.data?.message || 'Server error occurred'
    console.error(err)
  }
}
</script>
