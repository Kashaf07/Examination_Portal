<template>
  <div
    class="min-h-screen w-full bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 flex flex-col items-center py-10"
  >
    <div class="w-full max-w-full px-6">
      <!-- Back Button -->
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

      <h1
        class="text-3xl font-bold mb-6 text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-700 tracking-tight"
      >
        Applicant Attempts for Exam {{ examId }}
      </h1>

      <div
        v-if="error"
        class="mb-6 p-4 bg-red-100 text-red-700 border border-red-400 rounded-lg w-full"
      >
        {{ error }}
      </div>

      <div class="rounded-xl shadow-xl overflow-x-auto bg-white w-full">
        <table class="w-full border-separate border-spacing-0 min-w-[900px]">
          <thead>
            <tr class="bg-gradient-to-r from-blue-200 to-purple-200 text-blue-900 font-bold">
              <th class="px-6 py-4 w-24 text-left">Attempt ID</th>
              <th class="px-6 py-4 w-28 text-left">Applicant ID</th>
              <th class="px-6 py-4 w-64 text-left">Student Email</th>
              <th class="px-6 py-4 w-40 text-left">Start Time</th>
              <th class="px-6 py-4 w-40 text-left">End Time</th>
              <th class="px-6 py-4 w-32 text-right">Marks Obtained</th>
              <th class="px-6 py-4 w-24 text-right">Max Marks</th>
              <th class="px-6 py-4 w-28 text-center">Status</th>
              <th class="px-6 py-4 w-32 text-center">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="attempt in attempts"
              :key="attempt.Attempt_Id"
              class="hover:bg-blue-50 transition-colors duration-200 border-b border-gray-100"
            >
              <td class="px-6 py-3">{{ attempt.Attempt_Id }}</td>
              <td class="px-6 py-3">{{ attempt.Applicant_Id }}</td>
              <td class="px-6 py-3 break-words">{{ attempt.Student_Email || '-' }}</td>
              <td class="px-6 py-3">{{ attempt.Start_Time }}</td>
              <td class="px-6 py-3">{{ attempt.End_Time || '-' }}</td>
              <td class="px-6 py-3 text-right">{{ attempt.Marks_Obtained }}</td>
              <td class="px-6 py-3 text-right">{{ attempt.Max_Marks }}</td>
              <td class="px-6 py-3 text-center">
                <span
                  :class="{
                    'text-green-600 font-semibold': attempt.Status === 'Pass',
                    'text-red-500 font-semibold': attempt.Status === 'Fail',
                  }"
                >
                  {{ attempt.Status || '-' }}
                </span>
              </td>
              <td class="px-6 py-3 text-center">
                <button
                  @click="viewAnswers(attempt.Attempt_Id)"
                  class="bg-purple-600 hover:bg-purple-700 text-white px-5 py-2 rounded-full font-semibold shadow transition"
                >
                  View Answers
                </button>
              </td>
            </tr>
            <tr v-if="attempts.length === 0">
              <td colspan="9" class="text-center py-8 text-gray-500 italic"
                >No attempts found.</td
              >
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const examId = ref(route.params.examId)
const attempts = ref([])
const error = ref('')

const fetchAttempts = async () => {
  error.value = ''
  try {
    const response = await fetch(
      `http://localhost:5000/responses/api/attempts?exam_id=${examId.value}`
    )
    const data = await response.json()
    if (!response.ok) {
      error.value = data.error || 'Failed to load attempts'
    } else {
      attempts.value = data.attempts
    }
  } catch (e) {
    error.value = 'Error fetching attempts: ' + e.message
  }
}

const viewAnswers = (attemptId) => {
  router.push({ name: 'ViewAnswers', params: { attemptId } })
}

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

onMounted(() => {
  fetchAttempts()
})
</script>

<style scoped>
table {
  min-width: 900px; /* Prevents columns from squeezing too tightly */
}

@media (max-width: 900px) {
  table {
    min-width: 700px; /* Allows horizontal scrolling on smaller screens */
  }
}
</style>