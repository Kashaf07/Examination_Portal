<template>
  <div class="p-6">
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
            <th class="px-4 py-2">Total Questions</th>
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
                @click="navigateTo('AddQuestion', exam.Exam_Id)"
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
    AddQuestion: 'AddQuestion',
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

<style scoped>

/* Container */
.p-6 {
  padding: 1.5rem;
  background: linear-gradient(to bottom right, #E3F2FD, #F3E5F5, #FCE4EC);
  min-height: 100vh;
  font-family: 'Inter', sans-serif;
}

/* Heading */
h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  background: linear-gradient(to right, #2563eb, #4f46e5);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Create Exam Button */
button.bg-blue-600 {
  background: linear-gradient(to right, #2563eb, #4f46e5);
  padding: 0.5rem 1.25rem;
  border-radius: 1rem;
  font-weight: 600;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

button.bg-blue-600:hover {
  background: linear-gradient(to right, #1d4ed8, #4338ca);
  transform: scale(1.03);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
}

/* Table Styling */
table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 0 0 1px #e5e7eb, 0 6px 12px rgba(0, 0, 0, 0.04);
  background-color: white;
}

thead {
  background: linear-gradient(to right, #e0f2fe, #f0f9ff);
  color: #1e3a8a;
  font-weight: 600;
}

th, td {
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

tbody tr:hover {
  background-color: #f9fafb;
  transition: background 0.2s ease;
}

/* Action Buttons */
td button {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.4rem 0.75rem;
  border-radius: 0.75rem;
  transition: transform 0.2s ease;
}

td button:hover {
  transform: scale(1.05);
}

/* Individual Button Colors */
.bg-blue-500 {
  background: linear-gradient(to right, #3b82f6, #2563eb);
}
.bg-blue-500:hover {
  background: linear-gradient(to right, #2563eb, #1d4ed8);
}

.bg-green-500 {
  background: linear-gradient(to right, #22c55e, #16a34a);
}
.bg-green-500:hover {
  background: linear-gradient(to right, #16a34a, #15803d);
}

.bg-purple-500 {
  background: linear-gradient(to right, #a855f7, #7e22ce);
}
.bg-purple-500:hover {
  background: linear-gradient(to right, #7e22ce, #6b21a8);
}

/* No Exams Fallback */
.text-gray-500 {
  text-align: center;
  font-size: 1.125rem;
  padding: 2rem 0;
}

</style>
