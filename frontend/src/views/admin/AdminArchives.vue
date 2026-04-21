<template>
  <div class="min-h-screen w-full bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 flex flex-col items-center py-10">
    
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
                  class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg text-sm font-semibold shadow transition"
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
import axios from '../../utils/axiosInstance'
import { useRouter } from 'vue-router'

const router = useRouter()
const exams = ref([])
const searchQuery = ref('')
const showUnarchiveModal = ref(false)
const examToUnarchive = ref(null)

onMounted(fetchArchived)

async function fetchArchived() {
  const res = await axios.get('/admin/archived_exams')
  exams.value = res.data.exams
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
  router.push('/admin/exams')
}

function viewResponses(id) {
  localStorage.setItem('from_page', 'archives')

  router.push({
    name: 'ViewResponsesAdmin',
    params: { examId: id }
  })
}

async function unarchiveExam(id) {
  await axios.put(`/admin/exam/restore/${id}`)
  fetchArchived()
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
</style>
