<template>
  <div class="min-h-screen w-full bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 flex flex-col items-center py-10">
    
    <!-- Toast Notification -->
    <transition name="toast-slide">
      <div
        v-if="toast.show"
        class="fixed right-4 z-[9999] max-w-md"
        style="top: 80px;"
      >
        <div
          :class="[
            'p-4 rounded-xl shadow-2xl border-l-4',
            toast.type === 'error'
              ? 'bg-red-50 text-red-800 border-red-500'
              : 'bg-green-50 text-green-800 border-green-500'
          ]"
        >
          <div class="flex justify-between items-center">
            <div class="flex items-center gap-3">
              <!-- Error icon -->
              <svg v-if="toast.type === 'error'" class="h-5 w-5 text-red-500 shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM7.293 7.293a1 1 0 011.414 0L10 8.586l1.293-1.293a1 1 0 111.414 1.414L11.414 10l1.293 1.293a1 1 0 01-1.414 1.414L10 11.414l-1.293 1.293a1 1 0 01-1.414-1.414L8.586 10 7.293 8.707a1 1 0 010-1.414z"/>
              </svg>
              <!-- Success icon -->
              <svg v-else class="h-5 w-5 text-green-500 shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"/>
              </svg>
              <p class="text-sm font-medium">{{ toast.message }}</p>
            </div>
            <button @click="toast.show = false" class="text-gray-400 hover:text-gray-600 ml-4">
              <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 011.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Unarchive Confirmation Modal -->
    <div
      v-if="showUnarchiveModal"
      class="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-[9999] p-4"
      @click.self="showUnarchiveModal = false"
    >
      <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full p-8 text-center" style="animation: fadeIn 0.2s ease-out">
        <h2 class="text-2xl font-bold text-gray-800 mb-4">Unarchive Exam</h2>
        <p class="text-base text-gray-600 mb-8 leading-relaxed">
          Are you sure you want to unarchive <strong>{{ examToUnarchive?.Exam_Name }}</strong>? It will be moved back to conducted exams.
        </p>
        <div class="flex gap-4 justify-center">
          <button
            @click="showUnarchiveModal = false"
            class="flex-1 px-6 py-3 bg-white text-gray-700 border border-gray-300 rounded-full hover:bg-gray-50 transition-all font-semibold shadow"
          >
            Cancel
          </button>
          <button
            @click="confirmUnarchive"
            class="flex-1 px-6 py-3 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-all font-semibold shadow"
          >
            Unarchive
          </button>
        </div>
      </div>
    </div>

    <div class="w-full max-w-full px-6">

      <!-- BACK BUTTON -->
      <button
        @click="goBack"
        class="mb-6 flex items-center gap-2 px-4 py-2 bg-white/70 hover:bg-white/90 
               text-gray-800 rounded-lg shadow-md hover:shadow-lg transition-all duration-200 
               backdrop-blur-sm border border-gray-200"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
        </svg>
        <span class="font-semibold">Back</span>
      </button>

      <!-- GRADIENT TITLE -->
      <h1 class="text-3xl font-bold mb-6 bg-gradient-to-r from-blue-600 to-purple-700 bg-clip-text text-transparent">
        Past Exams
      </h1>

      <!-- SEARCH BOX (IMPROVED LIKE VIEW RESPONSES) -->
      <div class="mb-6 bg-white rounded-xl shadow-lg p-6">
        <input
          v-model="searchQuery"
          placeholder="🔍 Search by Exam Name, Date or Email..."
          class="w-full max-w-lg px-4 py-3 rounded-xl border-2 border-black bg-purple-50
                 focus:bg-white focus:ring-2 focus:ring-blue-400 outline-none transition 
                 text-sm font-medium placeholder:text-gray-600"
        />
      </div>

      <!-- TABLE -->
      <div class="rounded-xl shadow-xl overflow-x-auto bg-white w-full">
        <table class="w-full border-separate border-spacing-0">
          <thead>
            <tr class="bg-gradient-to-r from-blue-200 to-purple-200 text-blue-900 font-bold">
              <th class="px-4 py-3 text-left">Exam Name</th>
              <th class="px-4 py-3 text-left">Date</th>
              <th class="px-4 py-3 text-left">Total Applicants</th>
              <th class="px-4 py-3 text-left">Attempted</th>
              <th class="px-4 py-3 text-center">Actions</th>
              <th class="px-4 py-3 text-center">Unarchive</th>
            </tr>
          </thead>

          <tbody>
            <tr 
              v-for="exam in filteredExams" 
              :key="exam.Exam_Id"
              class="hover:bg-blue-50 border-b border-gray-100"
            >
              <td class="px-4 py-3">{{ exam.Exam_Name }}</td>
              <td class="px-4 py-3">{{ formatDate(exam.Exam_Date) }}</td>
              <td class="px-4 py-3">{{ exam.total_applicants }}</td>
              <td class="px-4 py-3">{{ exam.attempted_applicants }}</td>

              <td class="px-4 py-3 text-center">
                <button
                  @click="viewResponses(exam.Exam_Id)"
                  class="bg-purple-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-purple-700 shadow-md hover:shadow-lg transition font-semibold"
                >
                  View Responses
                </button>
              </td>

              <td class="px-4 py-3 text-center">
                <button
                  @click="promptUnarchive(exam)"
                  class="p-1 text-gray-600 hover:text-green-600 transition-all duration-200 hover:scale-110"
                  title="Unarchive"
                >
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <!-- box outline -->
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M3 9h18v11a1 1 0 01-1 1H4a1 1 0 01-1-1V9z"/>
                    <!-- lid top bar -->
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M3 9l1.5-4h15L21 9"/>
                    <!-- arrow up out of box -->
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 16v-4m0 0l-2 2m2-2l2 2"/>
                  </svg>
                </button>
              </td>
            </tr>

            <tr v-if="filteredExams.length === 0">
              <td colspan="6" class="text-center py-6 text-gray-500 italic">
                No archived exams found
              </td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from '../utils/axiosInstance'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const exams = ref([])
const searchQuery = ref('')
const showUnarchiveModal = ref(false)
const examToUnarchive = ref(null)
const toast = ref({ show: false, message: '', type: 'success' })
const callerRole = computed(() => route.query.role || 'Admin')

onMounted(fetchArchived)

async function fetchArchived() {
  try {
    const isFaculty = callerRole.value === 'Faculty'
    const url = isFaculty ? '/faculty/archived_exams' : '/admin/archived_exams'
    const res = await axios.get(url)
    exams.value = res.data.exams || []
  } catch (e) {
    console.error("Failed to fetch archived exams:", e)
  }
}

async function unarchiveExam(id) {
  try {
    const isfaculty = callerRole.value === 'Faculty'
    const url = isfaculty ? `/faculty/exam/restore/${id}` : `/admin/exam/restore/${id}`
    await axios.put(url)
    showToast('Exam unarchived successfully!', 'success')
    fetchArchived()
  } catch (e) {
    console.error("Failed to unarchive exam:", e)
    showToast('Failed to unarchive exam', 'error')
  }
}

function showToast(message, type = 'success') {
  toast.value.message = message
  toast.value.type = type
  toast.value.show = true
  setTimeout(() => { toast.value.show = false }, 3000)
}

/* 🔥 SMART SEARCH (LIKE VIEW RESPONSES) */
const filteredExams = computed(() => {
  return exams.value.filter(e => {
    const query = searchQuery.value.toLowerCase()

    const nameMatch = e.Exam_Name.toLowerCase().includes(query)
    const dateMatch = formatDate(e.Exam_Date).toLowerCase().includes(query)
    const emailMatch = (e.Faculty_Email || '').toLowerCase().includes(query)

    return nameMatch || dateMatch || emailMatch
  })
})

function formatDate(date) {
  return new Date(date).toLocaleDateString()
}

function goBack() {
  if (callerRole.value === 'Faculty') {
    router.push('/faculty')
  } else {
    router.push('/admin/exams')
  }
}

function viewResponses(id) {
  localStorage.setItem('from_page', 'archives')
  const routeName = callerRole.value === 'Faculty' 
    ? 'ViewResponses' 
    : 'ViewResponsesAdmin'
  router.push({
    name: routeName,
    params: { examId: id },
    query: { from: 'archives' }
  })
}

function promptUnarchive(exam) {
  examToUnarchive.value = exam
  showUnarchiveModal.value = true
}

async function confirmUnarchive() {
  showUnarchiveModal.value = false
  await unarchiveExam(examToUnarchive.value.Exam_Id)
  examToUnarchive.value = null
}
</script>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.95); }
  to   { opacity: 1; transform: scale(1); }
}

.toast-slide-enter-active, .toast-slide-leave-active { 
  transition: all 0.3s ease; 
}
.toast-slide-enter-from, .toast-slide-leave-to { 
  opacity: 0; 
  transform: translateX(60px); 
}
</style>
