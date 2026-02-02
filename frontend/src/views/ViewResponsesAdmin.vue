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
              v-for="(attempt, index) in paginatedAttempts"
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

        <!-- Pagination Controls -->
        <div v-if="attempts.length > 0" class="bg-gray-50 px-6 py-4 border-t border-gray-200">
          <div class="flex items-center justify-between">
            
            <!-- Results Info -->
            <div class="text-sm text-gray-700">
              Showing 
              <span class="font-semibold">{{ startIndex + 1 }}</span>
              to 
              <span class="font-semibold">{{ endIndex }}</span>
              of 
              <span class="font-semibold">{{ totalAttempts }}</span>
              results
            </div>

            <!-- Pagination Buttons -->
            <div class="flex items-center gap-2">
              
              <!-- Previous Button -->
              <button
                @click="goToPage(currentPage - 1)"
                :disabled="currentPage === 1"
                class="px-3 py-2 rounded-lg border border-gray-300 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
                </svg>
              </button>

              <!-- First Page -->
              <button
                v-if="showFirstPage"
                @click="goToPage(1)"
                class="px-4 py-2 rounded-lg border transition"
                :class="currentPage === 1 
                  ? 'bg-blue-600 text-white border-blue-600' 
                  : 'border-gray-300 bg-white hover:bg-gray-50'"
              >
                1
              </button>

              <!-- Left Ellipsis -->
              <span v-if="showLeftEllipsis" class="px-2 text-gray-500">...</span>

              <!-- Page Numbers -->
              <button
                v-for="page in visiblePages"
                :key="page"
                @click="goToPage(page)"
                class="px-4 py-2 rounded-lg border transition"
                :class="currentPage === page 
                  ? 'bg-blue-600 text-white border-blue-600' 
                  : 'border-gray-300 bg-white hover:bg-gray-50'"
              >
                {{ page }}
              </button>

              <!-- Right Ellipsis -->
              <span v-if="showRightEllipsis" class="px-2 text-gray-500">...</span>

              <!-- Last Page -->
              <button
                v-if="showLastPage"
                @click="goToPage(totalPages)"
                class="px-4 py-2 rounded-lg border transition"
                :class="currentPage === totalPages 
                  ? 'bg-blue-600 text-white border-blue-600' 
                  : 'border-gray-300 bg-white hover:bg-gray-50'"
              >
                {{ totalPages }}
              </button>

              <!-- Next Button -->
              <button
                @click="goToPage(currentPage + 1)"
                :disabled="currentPage === totalPages"
                class="px-3 py-2 rounded-lg border border-gray-300 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                </svg>
              </button>

            </div>
          </div>
        </div>
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

// ================= PAGINATION STATE =================
const currentPage = ref(1)
const itemsPerPage = ref(15)

// ================= PAGINATION COMPUTED =================
const totalAttempts = computed(() => attempts.value.length)

const totalPages = computed(() => Math.ceil(totalAttempts.value / itemsPerPage.value))

const paginatedAttempts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return attempts.value.slice(start, end)
})

const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage.value)

const endIndex = computed(() => {
  const end = currentPage.value * itemsPerPage.value
  return end > totalAttempts.value ? totalAttempts.value : end
})

// Google-style pagination
const visiblePages = computed(() => {
  const pages = []
  const maxVisible = 5
  
  let start = Math.max(2, currentPage.value - 2)
  let end = Math.min(totalPages.value - 1, currentPage.value + 2)
  
  if (currentPage.value <= 3) {
    end = Math.min(maxVisible, totalPages.value - 1)
    start = 2
  }
  
  if (currentPage.value >= totalPages.value - 2) {
    start = Math.max(2, totalPages.value - maxVisible + 1)
    end = totalPages.value - 1
  }
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
})

const showFirstPage = computed(() => {
  return totalPages.value > 1 && !visiblePages.value.includes(1)
})

const showLastPage = computed(() => {
  return totalPages.value > 1 && !visiblePages.value.includes(totalPages.value)
})

const showLeftEllipsis = computed(() => {
  return visiblePages.value.length > 0 && visiblePages.value[0] > 2
})

const showRightEllipsis = computed(() => {
  return visiblePages.value.length > 0 && visiblePages.value[visiblePages.value.length - 1] < totalPages.value - 1
})

// ================= PAGINATION METHODS =================
const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

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
      currentPage.value = 1 // Reset to first page when data refreshes
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

/* Smooth transitions for pagination buttons */
button {
  transition: all 0.2s ease;
}

button:hover:not(:disabled) {
  transform: translateY(-1px);
}

button:active:not(:disabled) {
  transform: translateY(0);
}
</style>