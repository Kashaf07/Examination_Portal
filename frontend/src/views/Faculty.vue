<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold mb-6">Welcome, {{ name }}</h1>
      <button 
      v-if="canSwitch"
      @click="switchRole"
      class="bg-purple-500 text-white px-4 py-2 rounded-lg"
      >
        Switch to Admin
      </button>
      <button
        @click="logout"
        class="logout-btn"
      >
        Logout
      </button>
    </div>

    <!-- Button Group -->
    <div class="flex gap-4 mb-6">
      <button
        @click="toggleExamForm"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        {{ showForm ? 'Close' : 'Create Exam' }}
      </button>
      <button
      @click="navigateTo('Groups')"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Groups
      </button>
      <button
      @click="navigateTo('AddApplicants')"
      class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
      Add Applicants
    </button>

      <button
        @click="navigateTo('UploadStudents')"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Upload Applicants
      </button>
    </div>

    <!-- Create Exam Form -->
    <div v-if="showForm" class="bg-white shadow rounded p-4 max-w-3xl mb-8">
      <h2 class="text-xl font-semibold mb-4">Create Exam</h2>
      <form @submit.prevent="submitExam">
        <div class="grid grid-cols-2 gap-4">
          <input v-model="exam.exam_name" type="text" placeholder="Exam Name" required class="border p-2 rounded" />
          <input v-model="exam.exam_date" type="date" placeholder="Exam Date" required class="border p-2 rounded" :min="todayDate" />
          <input v-model="exam.exam_time" type="time" placeholder="Exam Time" required class="border p-2 rounded" />
          <input v-model="exam.duration" type="number" placeholder="Duration (Minutes)" required class="border p-2 rounded" />
          <input v-model="exam.total_questions" type="number" placeholder="Total Questions" required class="border p-2 rounded" />
          <input v-model="exam.max_marks" type="number" placeholder="Max Marks" required class="border p-2 rounded" />
        </div>
        <button type="submit" class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 mt-4">
          Submit Exam
        </button>
        <p v-if="examSubmitMessage" class="mt-2 text-sm text-red-600">{{ examSubmitMessage }}</p>
      </form>
    </div>

    

    <!-- Exam Table (Upcoming/Created) -->
    <div v-if="createdExams.length" class="mt-8">
      <h2 class="text-2xl font-semibold mb-4">Created Exams</h2>
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
          <tr v-for="exam in createdExams" :key="exam.Exam_Id" class="border-t">
            <td class="px-4 py-2">{{ exam.Exam_Name }}</td>
            <td class="px-4 py-2">{{ exam.Exam_Date }}</td>
            <td class="px-4 py-2">{{ exam.Exam_Time }}</td>
            <td class="px-4 py-2">{{ exam.Duration_Minutes }}</td>
            <td class="px-4 py-2">{{ exam.Total_Questions }}</td>
            <td class="px-4 py-2">{{ exam.Max_Marks }}</td>
            <td class="px-4 py-3">
  <div class="flex flex-wrap justify-center items-center gap-2">

    <!-- Add Students -->
    <button
      @click="navigateTo('AddApplicants_exam', exam.Exam_Id)"
      class="flex items-center gap-1 bg-blue-500 text-white px-3 py-1.5 rounded-full text-xs shadow hover:scale-105 transition"
    >
      Add Students
    </button>

    <!-- Add Question Bank -->
    <button
      @click="navigateTo('AddQuestion', exam.Exam_Id)"
      class="flex items-center gap-1 bg-green-500 text-white px-3 py-1.5 rounded-full text-xs shadow hover:scale-105 transition"
    >
      Question Bank
    </button>

    <!-- QB Status Icon -->
    <span
      v-if="examStatus[exam.Exam_Id]?.has_question_bank"
      class="text-green-600 text-lg"
      title="Completed"
    >
      ✔
    </span>
    <span
      v-else
      class="text-yellow-600 text-lg"
      title="Pending"
    >
      ⏳
    </span>

    <!-- Make Question Paper -->
    <button
      @click="navigateTo('MakeQuestionPaper', exam.Exam_Id)"
      class="flex items-center gap-1 bg-purple-500 text-white px-3 py-1.5 rounded-full text-xs shadow hover:scale-105 transition"
    >
     Question Paper
    </button>

    <!-- Paper Status Icon -->
    <span
      v-if="examStatus[exam.Exam_Id]?.has_question_paper"
      class="text-green-600 text-lg"
      title="Completed"
    >
      ✔
    </span>
    <span
      v-else
      class="text-yellow-600 text-lg"
      title="Pending"
    >
      ⏳
    </span>

    <!-- Delete (LAST BUTTON) -->
    <button
      @click="deleteExam(exam.Exam_Id)"
      class="flex items-center gap-1 bg-red-500 text-white px-3 py-1.5 rounded-full text-xs shadow hover:scale-105 transition"
    >
      🗑 Delete
    </button>

  </div>
</td>

          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="mt-8 text-gray-500 text-center text-lg">No exams created yet.</div>

    <!-- Conducted Exams Table -->
    <div v-if="conductedExams && conductedExams.length" class="mt-12">
      <h2 class="text-2xl font-semibold mb-4">Conducted Exams</h2>
      <table class="min-w-full border text-sm text-left">
        <thead class="bg-gray-200">
          <tr>
            <th class="px-4 py-2">Exam Name</th>
            <th class="px-4 py-2">Date</th>
            <th class="px-4 py-2">Total Applicants</th>
            <th class="px-4 py-2">Applicants Attempted</th>
            <th class="px-4 py-2 text-center">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="exam in conductedExams" :key="exam.Exam_Id" class="border-t">
            <td class="px-4 py-2">{{ exam.Exam_Name || 'N/A' }}</td>
            <td class="px-4 py-2">{{ formatDate(exam.Exam_Date) }}</td>
            <td class="px-4 py-2">{{ exam.total_applicants || 0 }}</td>
            <td class="px-4 py-2">{{ exam.attempted_applicants || 0 }}</td>
            <td class="px-4 py-2 text-center">
              <button
                @click="navigateTo('ViewResponses', exam.Exam_Id)"
                class="bg-purple-600 text-white px-3 py-1 rounded text-sm hover:bg-purple-700"
              >
                View Responses
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="mt-8 text-gray-500 text-center text-lg">
      No exams conducted yet.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from '../utils/axiosInstance'

const router = useRouter()

// ---------------------
// NEW STORAGE SYSTEM
// ---------------------
const roles = JSON.parse(localStorage.getItem("roles") || "[]")
const activeRole = ref(localStorage.getItem("active_role"))
const canSwitch = roles.includes("Admin") && roles.includes("Faculty")

// Switch Role Button
const switchRole = () => {
  const newRole = activeRole.value === "Faculty" ? "Admin" : "Faculty"
  localStorage.setItem("active_role", newRole)
  activeRole.value = newRole
  router.push(`/${newRole.toLowerCase()}`)
}

// ---------------------
// USER INFO
// ---------------------
const name = ref(localStorage.getItem("name"))
const email = localStorage.getItem("email")

// ---------------------
// OLD faculty_email → NEW email
// ---------------------
const facultyEmail = email

// ---------------------
// AUTH CHECK ON MOUNT
// ---------------------
onMounted(() => {
  console.log("FACULTY EMAIL:", facultyEmail)
  console.log("DEBUG: activeRole =", activeRole.value)
  console.log("DEBUG: facultyEmail =", facultyEmail)
  if (activeRole.value !== "Faculty") {
    router.push("/")
  } else {
    fetchExamsAndCategorize()
  }
})

// ---------------------
// EXAM DATA
// ---------------------

const showForm = ref(false)
const showApplicantForm = ref(false)
const submitMessage = ref('')
const examSubmitMessage = ref('')
const createdExams = ref([])
const conductedExams = ref([])
const examStatus = ref({})

const todayDate = computed(() => {
  const today = new Date()
  const year = today.getFullYear()
  const month = String(today.getMonth() + 1).padStart(2, '0')
  const day = String(today.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
})

const exam = ref({
  exam_name: '',
  exam_date: '',
  exam_time: '',
  duration: '',
  total_questions: '',
  max_marks: '',
  faculty_email: facultyEmail
})

const applicant = ref({
  Full_Name: '',
  Email: '',
  Password: '',
  Phone: '',
  DOB: '',
  Gender: '',
  Address: ''
})

const toggleExamForm = () => {
  showForm.value = !showForm.value
  examSubmitMessage.value = ''
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}

const getExamEndTime = (exam) => {
  if (!exam.Exam_Date || !exam.Exam_Time || !exam.Duration_Minutes) return null
  const start = new Date(`${exam.Exam_Date}T${exam.Exam_Time}`)
  return new Date(start.getTime() + Number(exam.Duration_Minutes) * 60000)
}

const loadExamStatuses = async (exams) => {
  const statusMap = {}
  for (const exam of exams) {
    try {
      const res = await axios.get(`/exam/status/${exam.Exam_Id}`)
      statusMap[exam.Exam_Id] = res.data.success ? res.data.status : { has_question_bank: false, has_question_paper: false }
    } catch {
      statusMap[exam.Exam_Id] = { has_question_bank: false, has_question_paper: false }
    }
  }
  examStatus.value = statusMap
}

const fetchExamsAndCategorize = async () => {
  console.log("DEBUG: Fetching exams for →", facultyEmail)
  try {
    const res = await axios.get(`/exam/get_exams/${facultyEmail}`)
    console.log("DEBUG: /exam/get_exams response →", res.data)
    if (res.data.success) {
      const now = new Date()
      const allExams = res.data.exams || []

      createdExams.value = allExams.filter(exam => now < getExamEndTime(exam))
      conductedExams.value = allExams.filter(exam => now >= getExamEndTime(exam))

      await loadExamStatuses(createdExams.value)
    }

    const conductedRes = await axios.get(`/faculty/conducted_exams/${facultyEmail}`)
    if (conductedRes.data.success) {
      conductedExams.value = conductedRes.data.exams
    }
  } catch (err) {
    console.error('Failed to fetch exams', err)
  }
}

const submitExam = async () => {
  try {
    const res = await axios.post('/exam/create', exam.value)
    if (res.data.success) {
      examSubmitMessage.value = 'Exam created successfully!'
      showForm.value = false
      fetchExamsAndCategorize()

      exam.value = {
        exam_name: '',
        exam_date: '',
        exam_time: '',
        duration: '',
        total_questions: '',
        max_marks: '',
        faculty_email: facultyEmail
      }
    } else {
      examSubmitMessage.value = res.data.message || 'Failed to create exam.'
    }
  } catch {
    examSubmitMessage.value = 'Error creating exam.'
  }
}

const submitApplicant = async () => {
  try {
    const res = await axios.post('/applicants/add', applicant.value)
    submitMessage.value = res.data.success ? 'Applicant added successfully!' : 'Failed to add applicant.'
  } catch {
    submitMessage.value = 'Error occurred while adding applicant.'
  }
}

const navigateTo = (action, examId) => {
  const routeMap = {
    AddApplicants_exam: 'AddApplicantsExam',
    AddApplicants: 'AddApplicants',
    AddQuestion: 'AddQuestion',
    MakeQuestionPaper: 'MakeQuestionPaper',
    UploadStudents: 'UploadStudents',
    ViewResponses: 'ViewResponses',
    Groups: 'FacultyGroups'
  }
  examId
    ? router.push({ name: routeMap[action], params: { examId } })
    : router.push({ name: routeMap[action] })
}

const logout = async () => {
  try {
    await axios.post('/auth/logout', {
      email,
      role: activeRole.value
    })

    localStorage.clear()
    router.push('/')
  } catch {
    alert('Logout failed. Try again.')
  }
}
</script>


<style scoped>
.p-6 {
  padding: 1.5rem;
  background: linear-gradient(to bottom right, #E3F2FD, #F3E5F5, #FCE4EC);
  min-height: 100vh;
  font-family: 'Inter', sans-serif;
}
h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  background: linear-gradient(to right, #2563eb, #4f46e5);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
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
.logout-btn {
  background: linear-gradient(to right, #ef4444, #b51a1a);
  padding: 0.5rem 1.25rem;
  border-radius: 1rem;
  font-weight: 600;
  color: white;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
}
.logout-btn:hover {
  background: linear-gradient(to right, #c02323, #991b1b);
  transform: scale(1.03);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
}
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
.text-gray-500 {
  text-align: center;
  font-size: 1.125rem;
  padding: 2rem 0;
}
.bg-red-500 {
  background: linear-gradient(to right, #ef4444, #dc2626);
}
.bg-red-500:hover {
  background: linear-gradient(to right, #dc2626, #b91c1c);
}
.inline-block {
  font-weight: 600;
}
</style>
