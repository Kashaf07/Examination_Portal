<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">Welcome, {{ facultyName }}</h1>

    <button @click="showForm = true"
            v-if="!showForm"
            class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 mb-6">
      Create Exam
    </button>

    <CreateExamForm v-if="showForm" @closeForm="onFormClose" />

    <div v-if="exams.length" class="mt-8">
      <h2 class="text-2xl font-semibold mb-4">Your Exams</h2>
      <table class="min-w-full border text-sm text-left">
        <thead class="bg-gray-200">
          <tr>
            <th class="px-4 py-2">Exam Name</th>
            <th class="px-4 py-2">Date</th>
            <th class="px-4 py-2">Time</th>
            <th class="px-4 py-2">Duration (Min)</th>
            <th class="px-4 py-2">Total Qs</th>
            <th class="px-4 py-2">Max Marks</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="exam in exams" :key="exam.Exam_Id" class="border-t">
            <td class="px-4 py-2">{{ exam.Exam_Name }}</td>
            <td class="px-4 py-2">{{ exam.Exam_Date }}</td>
            <td class="px-4 py-2">{{ exam.Exam_Time }}</td>
            <td class="px-4 py-2">{{ exam.Duration_Minutes }}</td>
            <td class="px-4 py-2">{{ exam.Total_Questions }}</td>
            <td class="px-4 py-2">{{ exam.Max_Marks }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import CreateExamForm from '../components/CreateExamForm.vue'

const facultyName = ref('')
const facultyEmail = localStorage.getItem('faculty_email') || ''
const showForm = ref(false)
const exams = ref([])

const fetchExams = async () => {
  try {
    const res = await axios.get(`http://localhost:5000/api/exam/get_exams/${facultyEmail}`)
    if (res.data.success) {
      exams.value = res.data.exams
    }
  } catch (err) {
    console.error(err)
  }
}

const onFormClose = () => {
  showForm.value = false
  fetchExams()  // Refresh exam list
}

onMounted(() => {
  facultyName.value = localStorage.getItem('faculty_name') || 'Faculty'
  fetchExams()
})
</script>
