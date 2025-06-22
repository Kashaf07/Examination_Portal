<template>
  <div class="min-h-screen p-10 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
    <div class="text-center mb-6">
      <h2 class="text-4xl font-bold text-blue-800">🧑‍🎓 Add Applicants to Exam</h2>
      <p class="text-lg text-gray-600 mt-2">
        Exam ID: {{ examId }} | Exam Name: {{ examName || 'Loading...' }}
      </p>
    </div>

    <div class="max-w-4xl mx-auto bg-white p-10 rounded-2xl shadow-xl">
      <h3 class="text-xl font-semibold mb-4">All Applicants</h3>

      <div v-if="loadingApplicants" class="text-gray-600 mb-4">Loading applicants...</div>
      <div v-if="error" class="text-red-600 mb-4">{{ error }}</div>

      <ul v-else>
        <li
          v-for="applicant in applicants"
          :key="applicant.Applicant_Id"
          class="flex justify-between items-center py-2 border-b"
        >
          <span>{{ applicant.Full_Name }} ({{ applicant.Email }})</span>
          <div class="space-x-2">
            <button
              v-if="!isAdded(applicant.Applicant_Id)"
              @click="addApplicant(applicant.Applicant_Id)"
              class="bg-blue-500 text-white px-4 py-1 rounded hover:bg-blue-600"
            >
              Add
            </button>
            <button
              v-if="isAdded(applicant.Applicant_Id)"
              @click="removeApplicant(applicant.Applicant_Id)"
              class="bg-red-500 text-white px-4 py-1 rounded hover:bg-red-600"
            >
              Remove
            </button>
          </div>
        </li>
      </ul>

      <div class="mt-6 text-center">
        <p class="text-sm mb-2 text-gray-700">Selected: {{ selectedApplicants.length }} applicants</p>
        <button
          @click="confirmAdd"
          :disabled="selectedApplicants.length === 0"
          class="bg-purple-600 text-white px-6 py-2 rounded disabled:bg-gray-400"
        >
          Confirm
        </button>
      </div>

      <p v-if="message" class="mt-6 text-center text-green-700 font-semibold">{{ message }}</p>
      <p v-if="error" class="mt-6 text-center text-red-600 font-semibold">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const examId = route.params.examId
const examName = ref('')
const applicants = ref([])
const selectedApplicants = ref([])
const message = ref('')
const error = ref('')
const loadingApplicants = ref(true)

// Fetch exam name using ID
const fetchExamDetails = async () => {
  try {
    const res = await fetch(`http://localhost:5000/api/exam/get_exam_by_id/${examId}`)
    const data = await res.json()
    if (res.ok && data.exam) {
      examName.value = data.exam.Exam_Name
    } else {
      error.value = 'Failed to fetch exam name'
    }
  } catch (err) {
    console.error('Error fetching exam name:', err)
    error.value = 'Error loading exam details'
  }
}

// Fetch applicants
const fetchApplicants = async () => {
  loadingApplicants.value = true
  try {
    const res = await fetch('http://localhost:5000/api/applicants')
    const data = await res.json()
    if (res.ok && data.success && data.applicants) {
      applicants.value = data.applicants
    } else {
      error.value = data.error || 'Failed to load applicants'
    }
  } catch (err) {
    console.error('Error fetching applicants:', err)
    error.value = 'Error loading applicants'
  } finally {
    loadingApplicants.value = false
  }
}

// Selection logic
const addApplicant = (id) => {
  if (!selectedApplicants.value.includes(id)) {
    selectedApplicants.value.push(id)
  }
}
const removeApplicant = (id) => {
  selectedApplicants.value = selectedApplicants.value.filter(aid => aid !== id)
}
const isAdded = (id) => selectedApplicants.value.includes(id)

// Confirm assign
const confirmAdd = async () => {
  try {
    const res = await fetch('http://localhost:5000/api/assign_applicants', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        exam_id: examId,
        applicant_ids: selectedApplicants.value
      })
    })
    const result = await res.json()
    if (res.ok) {
      message.value = result.message
      selectedApplicants.value = []
    } else {
      error.value = result.error || 'Failed to assign applicants'
    }
  } catch (err) {
    console.error('Error assigning applicants:', err)
    error.value = 'Error assigning applicants'
  }
}

// Mount
onMounted(() => {
  fetchExamDetails()
  fetchApplicants()
})
</script>
