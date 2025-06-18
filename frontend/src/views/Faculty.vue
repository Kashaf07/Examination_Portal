<template>
  <div class="p-6 max-w-6xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">Welcome, {{ facultyName }}</h1>

    <button
      @click="showForm = true"
      v-if="!showForm"
      class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 mb-6"
    >
      Create Exam
    </button>

    <!-- Show Create Exam Form -->
    <CreateExamForm v-if="showForm" @closeForm="onFormClose" />

    <!-- Exam List -->
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
            <th class="px-4 py-2 text-center">Actions</th>
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
            <td class="px-4 py-2 text-center space-y-1 space-x-1">
              <button
                @click="navigateTo('AddStudents', exam.Exam_Id)"
                class="bg-blue-500 text-white px-2 py-1 rounded hover:bg-blue-600 text-xs"
              >
                Add Students
              </button>
              <button
                @click="navigateTo('AddQuestionBank', exam.Exam_Id)"
                class="bg-green-500 text-white px-2 py-1 rounded hover:bg-green-600 text-xs"
              >
                Add Question Bank
              </button>
              <button
                @click="navigateTo('MakeQuestionPaper', exam.Exam_Id)"
                class="bg-purple-500 text-white px-2 py-1 rounded hover:bg-purple-600 text-xs"
              >
                Make Question Paper
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- No exams fallback -->
    <div v-else class="mt-8 text-gray-500">No exams created yet.</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import CreateExamForm from '../components/CreateExamForm.vue'

const router = useRouter()

// Faculty Info
const facultyName = ref('')
const facultyEmail = localStorage.getItem('faculty_email') || ''

// UI State
const showForm = ref(false)
const exams = ref([])

// Fetch exams created by this faculty
const fetchExams = async () => {
  try {
    const res = await axios.get(`http://localhost:5000/api/exam/get_exams/${facultyEmail}`)
    if (res.data.success) {
      exams.value = res.data.exams
    }
  } catch (err) {
    console.error('Failed to fetch exams', err)
  }
}

// Called when form is closed to refresh the exam list
const onFormClose = () => {
  showForm.value = false
  fetchExams()
}

// Navigate to action pages with examId
const navigateTo = (action, examId) => {
  const routeMap = {
    AddStudents: 'AddStudents',
    AddQuestionBank: 'AddQuestionBank',
    MakeQuestionPaper: 'MakeQuestionPaper',
  }
  router.push({ name: routeMap[action], params: { examId } })
}

// Load on mount
onMounted(() => {
  facultyName.value = localStorage.getItem('faculty_name') || 'Faculty'
  fetchExams()
})
</script>
