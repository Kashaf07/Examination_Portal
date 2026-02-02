<template>
  <div class="min-h-screen p-10 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">

    <!-- BACK BUTTON -->
    <button
      @click="goBack"
      class="mb-6 flex items-center gap-2 px-4 py-2 bg-white/70 hover:bg-white/90 
             text-gray-800 rounded-lg shadow-md hover:shadow-lg transition-all duration-200 
             backdrop-blur-sm border border-gray-200"
    >
      ← Back
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

const route = useRoute()
const router = useRouter()
const examId = route.params.examId

const role = localStorage.getItem("active_role")
const email = localStorage.getItem("email")

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

/* NAVIGATION */
const goBack = () => {
  const activeRole = localStorage.getItem('active_role')
  if (activeRole === 'Admin') router.push('/admin/exams')
  else if (activeRole === 'Faculty') router.push('/faculty')
  else router.push('/')
}

/* EXAM */
const fetchExamDetails = async () => {
  const res = await fetch(`http://localhost:5000/api/exam/get_exam_by_id/${examId}`)
  const data = await res.json()
  if (data.exam) {
    examName.value = data.exam.Exam_Name
    examDate.value = data.exam.Exam_Date
    examTime.value = data.exam.Exam_Time
  }
}

/* GROUPS */
const fetchGroups = async () => {
  const res = await fetch(`http://localhost:5000/api/groups?role=${role}&email=${email}`)
  const data = await res.json()
  if (data.success) groups.value = data.groups
}

/* ADD GROUP */
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

  let newCount = 0

  data.applicants.forEach(app => {
    if (assignedApplicants.value.some(a => a.Applicant_Id === app.Applicant_Id)) return

assignedApplicants.value.push({
  ...app,
  Group_Name: groups.value.find(
    g => g.Group_Id === selectedGroupId.value
  )?.Group_Name || 'Unknown Group'
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
}

/* REMOVE */
const removeApplicant = (id) => {
  selectedApplicants.value =
    selectedApplicants.value.filter(a => a !== id)

  assignedApplicants.value =
    assignedApplicants.value.filter(
      a => a.Applicant_Id !== id || a.is_assigned === 1
    )
}

/* CONFIRM */
const confirmAdd = async () => {
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

    assignedApplicants.value.forEach(app => {
      if (selectedApplicants.value.includes(app.Applicant_Id)) {
        app.is_assigned = 1
      }
    })

    selectedApplicants.value = []
  }
}

/* EMAIL */
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

/* INIT */
onMounted(async () => {
  await fetchExamDetails()
  await fetchGroups()
})
</script>
