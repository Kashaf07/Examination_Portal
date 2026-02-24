<template>
  <div class="min-h-screen p-10 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
  <div
  v-if="!isAuthorized"
  class="max-w-3xl mx-auto mt-10 p-8 bg-red-50 border border-red-400 rounded-xl text-center"
>
  <h2 class="text-2xl font-bold text-red-700 mb-2">
    403 - Unauthorized
  </h2>
  <p class="text-red-600">
    {{ error }}
  </p>
</div>

    <!-- BACK BUTTON -->
    <button
  @click="goBack"
  class="mb-6 flex items-center gap-2 px-4 py-2 bg-white/70 hover:bg-white/90 
         text-gray-800 rounded-lg shadow-md hover:shadow-lg transition-all duration-200 
         backdrop-blur-sm border border-gray-200"
>
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    class="h-5 w-5" 
    viewBox="0 0 20 20" 
    fill="currentColor"
  >
    <path 
      fill-rule="evenodd" 
      d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" 
      clip-rule="evenodd" 
    />
  </svg>
  <span class="font-semibold">Back</span>
</button>

    <!-- Heading -->
    <div class="text-center mb-6">
      <h2 class="text-4xl font-bold text-blue-800">🧑‍🎓 Add Applicants to Exam</h2>
      <p class="text-lg text-gray-600 mt-2">
        Exam ID: {{ examId }} | Exam Name: {{ examName || 'Loading...' }}
      </p>
    </div>

    <div class="max-w-5xl mx-auto bg-white p-10 rounded-2xl shadow-xl">

      <!-- GROUP ASSIGNMENT -->
      <h3 class="text-xl font-semibold mb-4 text-purple-700">
        Assign by Group
      </h3>

      <div class="flex gap-4 mb-2">
        <select v-model="selectedGroupId" class="flex-1 border px-4 py-2 rounded">
          <option value="">-- Select Group --</option>
          <option v-for="g in groups" :key="g.Group_Id" :value="g.Group_Id">
            {{ g.Group_Name }}
          </option>
        </select>

        <button
          @click="addGroupApplicants"
          class="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded"
        >
          Add Group
        </button>
      </div>

      <p v-if="infoMessage" class="text-sm text-orange-600 mb-6">
        {{ infoMessage }}
      </p>

      <hr class="my-8" />

      <!-- APPLICANTS -->
      <h3 class="text-xl font-semibold mb-4">Applicants</h3>

      <ul v-if="assignedApplicants.length">
        <li
          v-for="app in assignedApplicants"
          :key="app.Applicant_Id"
          class="flex justify-between items-center py-2 border-b"
        >
          <span>
            {{ app.Full_Name }} ({{ app.Email }})
            <span class="text-sm text-gray-500 ml-2">
              • {{ app.Group_Name }}
            </span>
          </span>

          <!-- Assigned -->
          <span
            v-if="app.is_assigned === 1"
            class="text-green-600 font-semibold text-sm"
          >
            ✔ Assigned
          </span>

          <!-- New -->
          <button
            v-else
            @click="removeApplicant(app.Applicant_Id)"
            class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded"
          >
            Remove
          </button>
        </li>
      </ul>

      <p v-else class="text-gray-500 text-sm mb-6">
        No applicants loaded.
      </p>

      <!-- CONFIRM -->
      <div class="mt-6 text-center">
        <p class="text-sm mb-2 text-gray-700">
          Selected (new): {{ selectedApplicants.length }} applicants
        </p>

        <button
          @click="confirmAdd"
          :disabled="selectedApplicants.length === 0"
          class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded disabled:bg-gray-400"
        >
          Confirm Assignment
        </button>
      </div>

      <!-- SUCCESS -->
      <p v-if="message" class="mt-4 text-center text-green-600 font-semibold">
        {{ message }}
      </p>

      <!-- EMAIL -->
      <div
        v-if="assignedApplicants.some(a => a.is_assigned === 1)"
        class="mt-6 text-center"
      >
        <button
          v-if="!sendingEmails"
          @click="sendEmails"
          class="bg-green-600 hover:bg-green-700 text-white font-semibold px-6 py-2 rounded shadow"
        >
          📧 Send Email to Assigned Applicants
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from '@/utils/axiosInstance'

const route = useRoute()
const router = useRouter()
const examId = route.params.examId

const role = localStorage.getItem("active_role")
const email = localStorage.getItem("email")

const isAuthorized = ref(true)
const error = ref('')

const groups = ref([])
const selectedGroupId = ref('')

const assignedApplicants = ref([])
const selectedApplicants = ref([])

const examName = ref('')
const examDate = ref('')
const examTime = ref('')

const message = ref('')
const infoMessage = ref('')
const sendingEmails = ref(false)

/* ================== NAVIGATION ================== */
const goBack = () => {
  const activeRole = localStorage.getItem('active_role')
  if (activeRole === 'Admin') router.push('/admin/exams')
  else if (activeRole === 'Faculty') router.push('/faculty')
  else router.push('/')
}

/* ================== 🔐 AUTH CHECK ================== */
const checkAuthorization = async () => {
  try {
    const res = await axios.get('/exam/can-manage-applicants', {
      params: {
        exam_id: examId,
        email,
        role
      }
    })

    if (!res.data.success) {
      isAuthorized.value = false
      error.value = "Unauthorized Access. You are not allowed to manage this exam."
    }

  } catch (err) {
    isAuthorized.value = false
    error.value = "Unauthorized Access. You are not allowed to manage this exam."
  }
}

/* ================== EXAM DETAILS ================== */
const fetchExamDetails = async () => {
  try {
    const res = await axios.get(`/exam/get_exam_by_id/${examId}`)

    if (res.data.exam) {
      examName.value = res.data.exam.Exam_Name
      examDate.value = res.data.exam.Exam_Date
      examTime.value = res.data.exam.Exam_Time
    } else {
      isAuthorized.value = false
      error.value = "Exam not found."
    }

  } catch {
    isAuthorized.value = false
    error.value = "Exam not found."
  }
}

/* ================== GROUPS ================== */
const fetchGroups = async () => {
  try {
    const res = await axios.get('/groups', {
      params: { role, email }
    })

    if (res.data.success) {
      groups.value = res.data.groups
    }

  } catch (err) {
    console.error("Error loading groups")
  }
}

/* ================== ADD GROUP ================== */
const addGroupApplicants = async () => {
  infoMessage.value = ''

  if (!selectedGroupId.value) {
    infoMessage.value = 'Please select a group first.'
    return
  }

  try {
    const res = await axios.get(
      `/exam-groups/${selectedGroupId.value}/applicants`,
      {
        params: { exam_id: examId }
      }
    )

    const data = res.data

    if (!data.success) {
      infoMessage.value = data.message || 'Failed to load applicants'
      return
    }

    let newCount = 0

    data.applicants.forEach(app => {
      if (assignedApplicants.value.some(a => a.Applicant_Id === app.Applicant_Id)) return

      assignedApplicants.value.push({
        ...app,
        Group_Name:
          groups.value.find(g => g.Group_Id === selectedGroupId.value)
            ?.Group_Name || 'Unknown Group'
      })

      if (
        app.is_assigned === 0 &&
        !selectedApplicants.value.includes(app.Applicant_Id)
      ) {
        selectedApplicants.value.push(app.Applicant_Id)
        newCount++
      }
    })

    if (newCount === 0) {
      infoMessage.value = 'All applicants in this group are already assigned.'
    }

  } catch (err) {
    console.error("Error loading applicants")
  }
}

/* ================== REMOVE ================== */
const removeApplicant = (id) => {
  selectedApplicants.value =
    selectedApplicants.value.filter(a => a !== id)

  assignedApplicants.value =
    assignedApplicants.value.filter(
      a => a.Applicant_Id !== id || a.is_assigned === 1
    )
}

/* ================== CONFIRM ================== */
const confirmAdd = async () => {
  try {
    const res = await axios.post('/exam-groups/assign', {
      exam_id: examId,
      applicant_ids: selectedApplicants.value
    })

    const data = res.data

    if (data.success) {
      message.value =
        `${data.assigned_count} applicant(s) assigned successfully!`

      assignedApplicants.value.forEach(app => {
        if (selectedApplicants.value.includes(app.Applicant_Id)) {
          app.is_assigned = 1
        }
      })

      selectedApplicants.value = []
    } else {
      message.value =
        `Error: ${data.message || 'Failed to assign applicants'}`
    }

  } catch (err) {
    console.error("Error assigning applicants")
  }
}

/* ================== EMAIL ================== */
const sendEmails = async () => {
  sendingEmails.value = true

  await axios.post('/send_exam_emails', {
    exam: {
      Exam_Id: examId,
      Exam_Name: examName.value,
      Exam_Date: examDate.value,
      Exam_Time: examTime.value
    },
    applicants: assignedApplicants.value
  })

  sendingEmails.value = false
}

/* ================== INIT ================== */
onMounted(async () => {
  await checkAuthorization()

  if (!isAuthorized.value) return

  await fetchExamDetails()
  await fetchGroups()
})
</script>