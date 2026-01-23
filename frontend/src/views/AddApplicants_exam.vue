<template>
  <div class="min-h-screen p-10 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
    <!-- Heading -->
    <div class="text-center mb-6">
      <h2 class="text-4xl font-bold text-blue-800">🧑‍🎓 Add Applicants to Exam</h2>
      <p class="text-lg text-gray-600 mt-2">
        Exam ID: {{ examId }} | Exam Name: {{ examName || 'Loading...' }}
      </p>
    </div>

    <div class="max-w-5xl mx-auto bg-white p-10 rounded-2xl shadow-xl">

      <!-- ================= GROUP BASED ASSIGNMENT ================= -->
      <h3 class="text-xl font-semibold mb-4 text-purple-700">
        Assign by Group
      </h3>

      <select
        v-model="selectedGroupId"
        class="w-full border px-4 py-2 rounded mb-4"
      >
        <option disabled value="">-- Select Group --</option>
        <option v-for="g in groups" :key="g.Group_Id" :value="g.Group_Id">
          {{ g.Group_Name }}
        </option>
      </select>

      <ul v-if="groupApplicants.length" class="mb-4">
        <li
          v-for="ga in groupApplicants"
          :key="ga.Applicant_Id"
          class="py-1 border-b text-sm"
        >
          {{ ga.Full_Name }} ({{ ga.Email }})
        </li>
      </ul>

      <button
        v-if="selectedGroupId"
        @click="confirmGroupAssign"
        class="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded mb-8"
      >
        Confirm Group Assignment
      </button>

      <hr class="my-8" />

      <!-- ================= INDIVIDUAL APPLICANTS (OLD LOGIC) ================= -->
      <h3 class="text-xl font-semibold mb-4">All Applicants</h3>

      <div v-if="loadingApplicants" class="text-gray-600 mb-4">
        Loading applicants...
      </div>

      <div v-if="error" class="text-red-600 mb-4">
        {{ error }}
      </div>

      <ul v-if="!loadingApplicants">
        <li
          v-for="applicant in applicants"
          :key="applicant.Applicant_Id"
          class="flex justify-between items-center py-2 border-b"
        >
          <span>{{ applicant.Full_Name }} ({{ applicant.Email }})</span>

          <div class="space-x-2">
            <span
              v-if="isAlreadyAssigned(applicant.Applicant_Id)"
              class="text-green-600 font-semibold text-sm"
            >
              ✅ Already Assigned
            </span>

            <button
              v-else-if="!selectedApplicants.includes(applicant.Applicant_Id)"
              @click="toggleAdd(applicant.Applicant_Id)"
              class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded"
            >
              Add
            </button>

            <button
              v-else
              @click="toggleAdd(applicant.Applicant_Id)"
              class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded"
            >
              Remove
            </button>
          </div>
        </li>
      </ul>

      <!-- Confirm Individual -->
      <div class="mt-6 text-center">
        <p class="text-sm mb-2 text-gray-700">
          Selected: {{ selectedApplicants.length }} applicants
        </p>

        <button
          @click="confirmAdd"
          :disabled="selectedApplicants.length === 0"
          class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded disabled:bg-gray-400"
        >
          Confirm Individual Assignment
        </button>
      </div>

      <!-- Messages -->
      <p v-if="message" class="mt-4 text-center text-green-600 font-semibold">
        {{ message }}
      </p>
      <p v-if="error && !message" class="mt-4 text-center text-red-600 font-semibold">
        {{ error }}
      </p>

      <!-- Send Email -->
      <div v-if="assignedApplicants.length > 0" class="mt-4 text-center">
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
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const examId = route.params.examId

const role = localStorage.getItem("active_role")
const email = localStorage.getItem("email")

const applicants = ref([])
const selectedApplicants = ref([])
const assignedApplicants = ref([])

const groups = ref([])
const selectedGroupId = ref('')
const groupApplicants = ref([])

const examName = ref('')
const examDate = ref('')
const examTime = ref('')

const message = ref('')
const error = ref('')
const loadingApplicants = ref(true)
const sendingEmails = ref(false)

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
  const res = await fetch('http://localhost:5000/api/groups', {
    headers: { 'x-role': role, 'x-email': email }
  })
  const data = await res.json()
  if (data.success) groups.value = data.groups
}

const fetchGroupApplicants = async (groupId) => {
  const res = await fetch(`http://localhost:5000/api/groups/${groupId}/applicants`)
  const data = await res.json()
  if (data.success) groupApplicants.value = data.applicants
}

/* ---------------- APPLICANTS ---------------- */
const fetchAssignedApplicants = async () => {
  const res = await fetch(`http://localhost:5000/api/get_assigned_applicants/${examId}`)
  const data = await res.json()
  if (data.success) assignedApplicants.value = data.assignedApplicants
}

const fetchApplicants = async () => {
  loadingApplicants.value = true
  const res = await fetch('http://localhost:5000/api/applicants')
  const data = await res.json()
  if (data.success) applicants.value = data.applicants
  loadingApplicants.value = false
}

/* ---------------- ACTIONS ---------------- */
const toggleAdd = (id) => {
  selectedApplicants.value.includes(id)
    ? selectedApplicants.value = selectedApplicants.value.filter(i => i !== id)
    : selectedApplicants.value.push(id)
}

const isAlreadyAssigned = (id) =>
  assignedApplicants.value.some(a => a.Applicant_Id === id)

const confirmAdd = async () => {
  const res = await fetch('http://localhost:5000/api/assign_applicants', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ exam_id: examId, applicant_ids: selectedApplicants.value })
  })
  const data = await res.json()
  if (data.success) message.value = 'Applicants assigned successfully'
}

const confirmGroupAssign = async () => {
  const res = await fetch('http://localhost:5000/api/exam/assign-group', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ exam_id: examId, group_id: selectedGroupId.value })
  })
  const data = await res.json()
  if (data.success) message.value = `Group assigned (${data.assigned_count} applicants)`
}

const sendEmails = async () => {
  sendingEmails.value = true
  await fetch('http://localhost:5000/api/send_exam_emails', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      exam: { Exam_Id: examId, Exam_Name: examName.value, Exam_Date: examDate.value, Exam_Time: examTime.value },
      applicants: assignedApplicants.value
    })
  })
  sendingEmails.value = false
}

watch(selectedGroupId, val => val && fetchGroupApplicants(val))

onMounted(async () => {
  await fetchExamDetails()
  await fetchGroups()
  await fetchAssignedApplicants()
  await fetchApplicants()
})
</script>
