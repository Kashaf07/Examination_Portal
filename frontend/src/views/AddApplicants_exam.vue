<template>
  <div class="min-h-screen p-10 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">

    <!-- ✅ BACK BUTTON -->
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

      <!-- ================= GROUP ASSIGNMENT ================= -->
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

      <!-- ================= APPLICANTS ================= -->
      <h3 class="text-xl font-semibold mb-4">Applicants</h3>

      <ul v-if="assignedApplicants.length">
        <li
          v-for="app in assignedApplicants"
          :key="app.Applicant_Id"
          class="flex justify-between items-center py-2 border-b"
        >
          <span>
            {{ app.Full_Name }} ({{ app.Email }})
          </span>

          <!-- Already Assigned -->
          <span
            v-if="app.is_assigned === 1"
            class="text-green-600 font-semibold text-sm"
          >
            ✔ Assigned
          </span>

          <!-- Newly Added (before confirm) -->
          <button
            v-else-if="!isConfirmed"
            @click="removeApplicant(app.Applicant_Id)"
            class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded"
          >
            Remove
          </button>

          <!-- After Confirm -->
          <span
            v-else
            class="text-green-600 font-semibold text-sm"
          >
            ✔ Assigned
          </span>
        </li>
      </ul>

      <p v-else class="text-gray-500 text-sm mb-6">
        No applicants loaded.
      </p>

      <!-- ================= CONFIRM ================= -->
      <div class="mt-6 text-center">
        <p class="text-sm mb-2 text-gray-700">
          Selected (new): {{ selectedApplicants.length }} applicants
        </p>

        <button
          @click="confirmAdd"
          :disabled="selectedApplicants.length === 0 || isConfirmed"
          class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded disabled:bg-gray-400"
        >
          Confirm Assignment
        </button>
      </div>

      <!-- SUCCESS MESSAGE -->
      <p v-if="message" class="mt-4 text-center text-green-600 font-semibold">
        {{ message }}
      </p>

      <!-- ================= EMAIL (UNCHANGED) ================= -->
      <div
        v-if="assignedApplicants.length > 0 && isConfirmed"
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

const route = useRoute()
const router = useRouter()
const examId = route.params.examId

const role = localStorage.getItem("active_role")
const email = localStorage.getItem("email")

const groups = ref([])
const selectedGroupId = ref('')

const assignedApplicants = ref([])   // ALL applicants shown
const selectedApplicants = ref([])   // ONLY newly added ones

const examName = ref('')
const examDate = ref('')
const examTime = ref('')

const message = ref('')
const infoMessage = ref('')
const sendingEmails = ref(false)
const isConfirmed = ref(false)

/* ---------------- NAVIGATION ---------------- */
const goBack = () => {
  // Navigate based on active role
  const activeRole = localStorage.getItem('active_role')
  
  if (activeRole === 'Admin') {
    router.push('/admin/exams')
  } else if (activeRole === 'Faculty') {
    router.push('/faculty')
  } else {
    router.push('/')
  }
}
/* ---------------- EXAM ---------------- */
const fetchExamDetails = async () => {
  const res = await fetch(`http://localhost:5000/api/exam/get_exam_by_id/${examId}`)
  const data = await res.json()
  if (data.exam) {
    examName.value = data.exam.Exam_Name
    examDate.value = data.exam.Exam_Date
    examTime.value = data.exam.Exam_Time
  }
}

/* ---------------- GROUPS ---------------- */
const fetchGroups = async () => {
  const res = await fetch(
    `http://localhost:5000/api/groups?role=${role}&email=${email}`
  )
  const data = await res.json()
  if (data.success) groups.value = data.groups
}

/* ---------------- ADD GROUP APPLICANTS ---------------- */
const addGroupApplicants = async () => {
  infoMessage.value = ''

  if (!selectedGroupId.value) {
    infoMessage.value = 'Please select a group first.'
    return
  }

  const res = await fetch(
    `http://localhost:5000/api/groups/${selectedGroupId.value}/applicants?exam_id=${examId}`
  )
  const data = await res.json()

  if (!data.success || !Array.isArray(data.applicants)) {
    infoMessage.value = 'Failed to load applicants.'
    return
  }

  let newCount = 0

  data.applicants.forEach(app => {
    // Avoid duplicates in UI
    if (assignedApplicants.value.some(a => a.Applicant_Id === app.Applicant_Id)) return

    assignedApplicants.value.push(app)

    // Track only new ones for confirm
    if (app.is_assigned === 0) {
      selectedApplicants.value.push(app.Applicant_Id)
      newCount++
    }
  })

  if (newCount === 0) {
    infoMessage.value = 'All applicants in this group are already assigned.'
  }
}

/* ---------------- REMOVE (ONLY NEW) ---------------- */
const removeApplicant = (id) => {
  if (isConfirmed.value) return

  selectedApplicants.value =
    selectedApplicants.value.filter(a => a !== id)

  assignedApplicants.value =
    assignedApplicants.value.filter(
      a => a.Applicant_Id !== id || a.is_assigned === 1
    )
}

/* ---------------- CONFIRM ---------------- */
const confirmAdd = async () => {
  if (selectedApplicants.value.length === 0) return

  const res = await fetch('http://localhost:5000/api/assign_applicants', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      exam_id: examId,
      applicant_ids: selectedApplicants.value
    })
  })

  const data = await res.json()

  if (data.success) {
    message.value = 'Applicants assigned successfully'
    isConfirmed.value = true

    // Mark newly added as assigned
    assignedApplicants.value.forEach(app => {
      if (selectedApplicants.value.includes(app.Applicant_Id)) {
        app.is_assigned = 1
      }
    })

    selectedApplicants.value = []
  }
}

/* ---------------- EMAIL (UNCHANGED) ---------------- */
const sendEmails = async () => {
  sendingEmails.value = true
  await fetch('http://localhost:5000/api/send_exam_emails', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      exam: {
        Exam_Id: examId,
        Exam_Name: examName.value,
        Exam_Date: examDate.value,
        Exam_Time: examTime.value
      },
      applicants: assignedApplicants.value
    })
  })
  sendingEmails.value = false
}

/* ---------------- INIT ---------------- */
onMounted(async () => {
  await fetchExamDetails()
  await fetchGroups()
})
</script>