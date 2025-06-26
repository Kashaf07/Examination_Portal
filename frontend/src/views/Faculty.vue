<template>
  <div class="p-6">
    <h1 class="text-3xl font-bold mb-6">Welcome, {{ facultyName }}</h1>

    <!-- Button Group -->
    <div class="flex gap-4 mb-6">
      <button
        @click="toggleExamForm"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        {{ showForm ? 'Close' : 'Create Exam' }}
      </button>

      <button
        @click="showApplicantForm = !showApplicantForm"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        {{ showApplicantForm ? 'Close' : 'Add Applicants' }}
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
          <input v-model="exam.exam_date" type="date" placeholder="Exam Date" required class="border p-2 rounded" />
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

    <!-- Add Applicant Form -->
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

    <!-- Exam Table -->
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
                @click="navigateTo('AddApplicants_exam', exam.Exam_Id)"
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

    <div v-else class="mt-8 text-gray-500 text-center text-lg">No exams created yet.</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const facultyName = ref('')
const facultyEmail = localStorage.getItem('faculty_email') || ''

const showForm = ref(false)
const showApplicantForm = ref(false)
const exams = ref([])
const submitMessage = ref('')
const examSubmitMessage = ref('')

// Toggle exam form
const toggleExamForm = () => {
  showForm.value = !showForm.value
  examSubmitMessage.value = ''
}

// Create exam model
const exam = ref({
  exam_name: '',
  exam_date: '',
  exam_time: '',
  duration: '',
  total_questions: '',
  max_marks: '',
  faculty_email: facultyEmail
})

// Submit exam
const submitExam = async () => {
  try {
    const res = await axios.post('http://localhost:5000/api/exam/create', exam.value)
    if (res.data.success) {
      examSubmitMessage.value = 'Exam created successfully!'
      showForm.value = false
      fetchExams()
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
  } catch (err) {
    console.error('Error creating exam:', err)
    examSubmitMessage.value = 'Error occurred while creating exam.'
  }
}

// Submit applicant
const applicant = ref({
  Full_Name: '',
  Email: '',
  Password: '',
  Phone: '',
  DOB: '',
  Gender: '',
  Address: ''
})

const submitApplicant = async () => {
  try {
    const res = await axios.post('http://localhost:5000/api/applicants/add', applicant.value)
    if (res.data.success) {
      submitMessage.value = 'Applicant added successfully!'
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

// Navigation
const navigateTo = (action, examId) => {
  const routeMap = {
    AddApplicants_exam: 'AddApplicantsexam',
    AddQuestion: 'AddQuestion',
    MakeQuestionPaper: 'MakeQuestionPaper',
    UploadStudents: 'UploadStudents'
  }
  if (examId) {
    router.push({ name: routeMap[action], params: { examId } })
  } else {
    router.push({ name: routeMap[action] })
  }
}

// Init
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

