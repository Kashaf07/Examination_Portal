<template>
  <div class="p-6">
    <h1 class="text-3xl font-bold mb-6">Welcome, {{ facultyName }}</h1>

    <!-- Create Exam Button -->
    <button
      @click="showForm = true"
      v-if="!showForm"
      class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 mb-4"
    >
      Create Exam
    </button>

    <!-- Add Applicants Button -->
    <button
      @click="showApplicantForm = !showApplicantForm"
      class="bg-pink-600 text-white px-4 py-2 rounded hover:bg-pink-700 mb-6 ml-4"
    >
      {{ showApplicantForm ? 'Close' : 'Add Applicants' }}
    </button>

    <!-- Show Create Exam Form -->
    <CreateExamForm v-if="showForm" @closeForm="onFormClose" />

    <!-- Show Add Applicant Form -->
    <div v-if="showApplicantForm" class="bg-white shadow rounded p-4 max-w-xl mb-8">
      <h2 class="text-xl font-semibold mb-4">Add Applicant</h2>
      <form @submit.prevent="submitApplicant">
        <div class="grid grid-cols-2 gap-4">
          <input v-model="applicant.Full_Name" type="text" placeholder="Full Name" required class="border p-2 rounded" />
          <input v-model="applicant.Email" type="email" placeholder="Email" required class="border p-2 rounded" />
          <input v-model="applicant.Password" type="password" placeholder="Password" required class="border p-2 rounded" />
          <input v-model="applicant.Phone" type="text" placeholder="Phone" class="border p-2 rounded" />
          <input v-model="applicant.DOB" type="date" placeholder="DOB" class="border p-2 rounded" />
          <select v-model="applicant.Gender" class="border p-2 rounded">
            <option disabled value="">Select Gender</option>
            <option>Male</option>
            <option>Female</option>
            <option>Other</option>
          </select>
          <textarea v-model="applicant.Address" placeholder="Address" class="border p-2 rounded col-span-2"></textarea>
        </div>
        <button type="submit" class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 mt-4">
          Submit
        </button>
        <p v-if="submitMessage" class="mt-2 text-sm text-blue-700">{{ submitMessage }}</p>
      </form>
    </div>

    <!-- Exam List Table -->
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
            <td class="px-4 py-2 text-center space-x-1">
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

    <!-- No Exams Message -->
    <div v-else class="mt-8 text-gray-500 text-center text-lg">No exams created yet.</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import CreateExamForm from '../components/CreateExamForm.vue'

// Router
const router = useRouter()

// Faculty Info
const facultyName = ref('')
const facultyEmail = localStorage.getItem('faculty_email') || ''

// UI State
const showForm = ref(false)
const showApplicantForm = ref(false)
const exams = ref([])
const submitMessage = ref('')

// Applicant form model
const applicant = ref({
  Full_Name: '',
  Email: '',
  Password: '',
  Phone: '',
  DOB: '',
  Gender: '',
  Address: ''
})

// Fetch Exams
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

// Submit applicant
const submitApplicant = async () => {
  try {
    const res = await axios.post('http://localhost:5000/api/applicants/add', applicant.value)
    if (res.data.success) {
      submitMessage.value = 'Applicant added successfully!'
      // reset form
      applicant.value = {
        Full_Name: '',
        Email: '',
        Password: '',
        Phone: '',
        DOB: '',
        Gender: '',
        Address: ''
      }
    } else {
      submitMessage.value = 'Failed to add applicant.'
    }
  } catch (err) {
    console.error('Error adding applicant:', err)
    submitMessage.value = 'Error occurred while adding applicant.'
  }
}

// Form Close
const onFormClose = () => {
  showForm.value = false
  fetchExams()
}

// Navigate to route
const navigateTo = (action, examId) => {
  const routeMap = {
    AddStudents: 'AddStudents',
    AddQuestion: 'AddQuestion',
    MakeQuestionPaper: 'MakeQuestionPaper'
  }
  router.push({ name: routeMap[action], params: { examId } })
}

// On mount
onMounted(() => {
  facultyName.value = localStorage.getItem('faculty_name') || 'Faculty'
  fetchExams()
})
</script>

<style scoped>
/* Include your styles here or keep as-is */
</style>
