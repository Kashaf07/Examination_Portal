<template>
  <div
    v-if="!error"
    class="min-h-screen w-full bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 flex flex-col items-center py-10"
  >
    <div class="w-full max-w-full px-6">

      <!-- Back Button -->
      <button @click="goBack"
        class="mb-6 flex items-center gap-2 px-4 py-2 bg-white/70 hover:bg-white/90 text-gray-800 rounded-lg shadow-md hover:shadow-lg transition-all duration-200 backdrop-blur-sm border border-gray-200">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
        </svg>
        <span class="font-semibold">Back</span>
      </button>

      <!-- Title + Actions -->
      <div class="flex items-center justify-between mb-6">
        <h1 class="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-700 tracking-tight">
          Student Attempts for Exam {{ examId }}
        </h1>
        <div class="flex gap-4">
          <button @click="goToResult"
            class="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all duration-200 hover:scale-105">
            Result
          </button>
          <button @click="goToAnalytics"
            class="bg-purple-500 hover:bg-purple-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all duration-200 hover:scale-105">
            Analytics
          </button>
        </div>
      </div>

      <!-- TABLE -->
      <div class="rounded-xl shadow-xl overflow-x-auto bg-white w-full">
        <table class="w-full border-separate border-spacing-0 min-w-[1100px]">
          <thead>
            <tr class="bg-gradient-to-r from-blue-200 to-purple-200 text-blue-900 font-bold">
              <th class="px-4 py-4 text-left whitespace-nowrap">Attempt ID</th>

              <th class="px-4 py-4 text-left whitespace-nowrap">
                <div class="flex items-center gap-2">
                  Student ID
                  <svg @click.stop="openFilter($event,'student')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"
                    class="w-5 h-5 cursor-pointer flex-shrink-0"
                    :class="filters.studentId || filters.studentSort ? 'text-blue-600' : 'text-gray-500 hover:text-blue-600'">
                    <path d="M3 4h18l-7 8v6l-4 2v-8L3 4z"/>
                  </svg>
                </div>
              </th>

              <th class="px-4 py-4 text-left whitespace-nowrap">Student Email</th>
              <th class="px-4 py-4 text-left whitespace-nowrap">Start Time</th>
              <th class="px-4 py-4 text-left whitespace-nowrap">End Time</th>

              <th class="px-4 py-4 text-right whitespace-nowrap">
                <div class="flex items-center justify-end gap-2">
                  Marks Obtained
                  <svg @click.stop="openFilter($event,'marks')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"
                    class="w-5 h-5 cursor-pointer flex-shrink-0"
                    :class="filters.minMarks !== null || filters.marksSort ? 'text-blue-600' : 'text-gray-500 hover:text-blue-600'">
                    <path d="M3 4h18l-7 8v6l-4 2v-8L3 4z"/>
                  </svg>
                </div>
              </th>

              <th class="px-4 py-4 text-right whitespace-nowrap">Max Marks</th>

              <th class="px-4 py-4 text-center whitespace-nowrap">
                <div class="flex items-center justify-center gap-2">
                  Status
                  <svg @click.stop="openFilter($event,'status')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"
                    class="w-5 h-5 cursor-pointer flex-shrink-0"
                    :class="filters.status ? 'text-blue-600' : 'text-gray-500 hover:text-blue-600'">
                    <path d="M3 4h18l-7 8v6l-4 2v-8L3 4z"/>
                  </svg>
                </div>
              </th>

              <th class="px-4 py-4 text-center whitespace-nowrap">Key Activity</th>
              <th class="px-4 py-4 text-center whitespace-nowrap">Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="attempt in paginatedAttempts" :key="attempt.Attempt_Id"
              class="hover:bg-blue-50 border-b border-gray-100">

              <td class="px-4 py-3 whitespace-nowrap">{{ attempt.Attempt_Id }}</td>
              <td class="px-4 py-3 whitespace-nowrap">{{ attempt.Applicant_Id }}</td>
              <td class="px-4 py-3 text-sm break-all max-w-[160px]">{{ attempt.Student_Email || '-' }}</td>

              <td class="px-4 py-3 whitespace-nowrap">
                <span v-if="attempt.Start_Time" class="text-sm font-medium text-gray-800">{{ attempt.Start_Time }}</span>
                <span v-else class="text-gray-400">-</span>
              </td>

              <td class="px-4 py-3 whitespace-nowrap">
                <span v-if="attempt.End_Time && attempt.End_Time !== 'None'" class="text-sm font-medium text-gray-800">{{ attempt.End_Time }}</span>
                <span v-else class="text-gray-400">-</span>
              </td>

              <td class="px-4 py-3 text-right whitespace-nowrap">{{ attempt.Marks_Obtained }}</td>
              <td class="px-4 py-3 text-right whitespace-nowrap">{{ attempt.Max_Marks }}</td>

              <td class="px-4 py-3 text-center whitespace-nowrap">
                <span :class="{
                  'text-green-600 font-semibold': attempt.Status === 'Pass',
                  'text-red-500 font-semibold':   attempt.Status === 'Fail',
                  'text-amber-600 font-semibold':  attempt.Status === 'Restricted'
                }">{{ attempt.Status || '-' }}</span>
              </td>

              <!-- ✅ Key Activity -->
              <td class="px-4 py-3 text-center">
                <div v-if="!attempt.key_log_total || attempt.key_log_total === 0"
                  class="text-gray-400 text-sm italic">None</div>

                <div v-else class="relative flex flex-col items-center">
                  <button @click.stop="toggleKeyLog(attempt)"
                    class="inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-semibold border transition-all duration-200"
                    :class="attempt._showKeys
                      ? 'bg-indigo-600 text-white border-indigo-600 shadow-md'
                      : 'bg-white text-indigo-600 border-indigo-300 hover:bg-indigo-50'">
                    🔑 {{ attempt.key_log_total }}
                    <svg class="w-3 h-3 transition-transform duration-200"
                      :class="attempt._showKeys ? 'rotate-180' : ''"
                      fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
                    </svg>
                  </button>

                  <!-- Dropdown -->
                  <div v-if="attempt._showKeys"
                    class="absolute top-full mt-1 z-50 bg-white border border-gray-200 rounded-xl shadow-xl p-3 min-w-[220px] text-left"
                    style="white-space: nowrap;">
                    <div class="text-xs font-bold text-gray-500 mb-2 uppercase tracking-wide">Key Log Summary</div>
                    <div v-for="(s, i) in attempt.key_log_summary" :key="i"
                      class="flex items-center justify-between gap-3 py-1 border-b border-gray-50 last:border-0">
                      <span class="flex items-center gap-1 text-sm">
                        <span v-if="s.event_type === 'blocked'" class="text-red-500">🚫</span>
                        <span v-else-if="s.event_type === 'warning'" class="text-amber-500">⚠️</span>
                        <span v-else class="text-green-500">✅</span>
                        <span class="font-medium text-gray-700">{{ s.key_label }}</span>
                      </span>
                      <span class="text-xs font-bold text-gray-400 ml-2">×{{ s.count }}</span>
                    </div>
                    <div class="mt-2 pt-2 border-t border-gray-100 flex justify-between text-xs text-gray-400">
                      <span>Total keystrokes</span>
                      <span class="font-bold text-gray-600">{{ attempt.key_log_total }}</span>
                    </div>
                  </div>
                </div>
              </td>

              <td class="px-4 py-3 text-center whitespace-nowrap">
                <button @click="viewAnswers(attempt.Attempt_Id)"
                  class="bg-purple-600 hover:bg-purple-700 text-white px-5 py-2 rounded-full font-semibold shadow">
                  View Answers
                </button>
              </td>
            </tr>

            <tr v-if="filteredAttempts.length === 0">
              <td colspan="10" class="text-center py-8 text-gray-500 italic">No matching attempts found.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="flex justify-center items-center gap-3 mt-6">
        <button @click="currentPage--" :disabled="currentPage === 1"
          class="px-4 py-2 rounded-lg bg-white border border-gray-300 text-gray-700 font-semibold shadow hover:bg-blue-50 disabled:opacity-40 disabled:cursor-not-allowed transition">
          ← Prev
        </button>
        <span class="text-gray-600 font-medium">Page {{ currentPage }} of {{ totalPages }}</span>
        <button @click="currentPage++" :disabled="currentPage === totalPages"
          class="px-4 py-2 rounded-lg bg-white border border-gray-300 text-gray-700 font-semibold shadow hover:bg-blue-50 disabled:opacity-40 disabled:cursor-not-allowed transition">
          Next →
        </button>
      </div>
    </div>
  </div>

  <!-- FILTER POPUP -->
  <transition name="fade">
    <div v-if="activeFilter" :style="popoverStyle"
      class="filter-popup fixed bg-white shadow-2xl border border-gray-200 rounded-xl p-4 w-72 z-[9999] max-w-[95vw]">

      <div v-if="activeFilter === 'student'">
        <input v-model="filters.studentId" placeholder="Search Student ID"
          class="w-full border px-3 py-2 rounded-lg mb-3 focus:ring-2 focus:ring-blue-400 outline-none"/>
        <label class="text-xs text-gray-500 font-semibold block mb-2">Sort Student ID</label>
        <div class="flex justify-center gap-8 text-2xl font-bold">
          <span @click="toggleStudentSort('asc')"
            :class="filters.studentSort==='asc' ? 'text-blue-600 cursor-pointer' : 'text-gray-400 cursor-pointer hover:text-blue-600'">↑</span>
          <span @click="toggleStudentSort('desc')"
            :class="filters.studentSort==='desc' ? 'text-blue-600 cursor-pointer' : 'text-gray-400 cursor-pointer hover:text-blue-600'">↓</span>
        </div>
      </div>

      <div v-if="activeFilter === 'marks'">
        <label class="text-xs text-gray-500 font-semibold block mb-2">Minimum Marks</label>
        <input v-model.number="filters.minMarks" type="number" placeholder="Minimum Marks"
          class="w-full border px-3 py-2 rounded-lg mb-4 focus:ring-2 focus:ring-blue-400 outline-none"/>
        <label class="text-xs text-gray-500 font-semibold block mb-2">Sort Marks</label>
        <div class="flex justify-center gap-8 text-2xl font-bold">
          <span @click="toggleMarksSort('asc')"
            :class="filters.marksSort==='asc' ? 'text-blue-600 cursor-pointer' : 'text-gray-400 cursor-pointer hover:text-blue-600'">↑</span>
          <span @click="toggleMarksSort('desc')"
            :class="filters.marksSort==='desc' ? 'text-blue-600 cursor-pointer' : 'text-gray-400 cursor-pointer hover:text-blue-600'">↓</span>
        </div>
      </div>

      <div v-if="activeFilter === 'status'">
        <label class="text-xs text-gray-500 font-semibold block mb-3">Filter by Status</label>
        <div class="flex gap-3 flex-wrap">
          <button @click="filters.status = filters.status === 'Pass' ? '' : 'Pass'"
            class="flex-1 min-w-[90px] px-4 py-2 rounded-lg border font-semibold transition text-center"
            :class="filters.status === 'Pass' ? 'bg-green-600 text-white border-green-600' : 'bg-white text-green-600 border-green-400 hover:bg-green-50'">Pass</button>
          <button @click="filters.status = filters.status === 'Fail' ? '' : 'Fail'"
            class="flex-1 min-w-[90px] px-4 py-2 rounded-lg border font-semibold transition text-center"
            :class="filters.status === 'Fail' ? 'bg-red-600 text-white border-red-600' : 'bg-white text-red-600 border-red-400 hover:bg-red-50'">Fail</button>
          <button @click="filters.status = filters.status === 'Restricted' ? '' : 'Restricted'"
            class="flex-1 min-w-[90px] px-4 py-2 rounded-lg border font-semibold transition text-center"
            :class="filters.status === 'Restricted' ? 'bg-amber-500 text-white border-amber-500' : 'bg-white text-amber-600 border-amber-500 hover:bg-amber-50'">Restricted</button>
        </div>
      </div>

      <div class="flex justify-between mt-4">
        <button @click="applyFilter" class="text-sm text-blue-600 font-semibold">Apply</button>
        <button @click="clearCurrentFilter" class="text-sm text-red-500 font-semibold">Clear</button>
      </div>
    </div>
  </transition>

  <!-- UNAUTHORIZED -->
  <div v-if="error" class="min-h-screen flex items-center justify-center bg-red-50">
    <div class="bg-white shadow-xl rounded-xl p-8 text-center">
      <h2 class="text-2xl font-bold text-red-600 mb-4">Unauthorized Access</h2>
      <p class="text-gray-600 mb-6">You are not allowed to access this exam.</p>
      <button @click="router.back()"
        class="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-lg font-semibold shadow-md transition">
        Go Back
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
// ✅ Raw axios with explicit full URL — no axiosInstance baseURL interference
import axios from 'axios'

const route  = useRoute()
const router = useRouter()

const examId   = ref(route.params.examId)
const attempts = ref([])
const error    = ref('')

const currentPage  = ref(1)
const itemsPerPage = ref(15)
const activeFilter = ref(null)
const popoverStyle = ref({})

// ✅ CHANGE THIS if your backend runs on a different port/host
const API_BASE = '`http://${window.location.hostname}:5000/api`'

const filters = ref({
  studentId: '', minMarks: null, status: '', marksSort: '', studentSort: ''
})

const goToResult   = () => router.push({ name: 'ExamResult',    params: { examId: examId.value } })
const goToAnalytics = () => router.push({ name: 'ExamAnalytics', params: { examId: examId.value } })

const openFilter = (event, type) => {
  activeFilter.value = type
  const rect = event.target.getBoundingClientRect()
  let left = rect.left, top = rect.bottom + 8
  const popupWidth = 288, padding = 16
  if (left + popupWidth > window.innerWidth - padding) left = window.innerWidth - popupWidth - padding
  if (left < padding) left = padding
  popoverStyle.value = { top: `${top}px`, left: `${left}px` }
}

const toggleStudentSort = (dir) => { filters.value.studentSort = filters.value.studentSort === dir ? '' : dir; filters.value.marksSort = '' }
const toggleMarksSort   = (dir) => { filters.value.marksSort   = filters.value.marksSort   === dir ? '' : dir; filters.value.studentSort = '' }
const applyFilter       = ()    => { currentPage.value = 1; activeFilter.value = null }

const clearCurrentFilter = () => {
  if (activeFilter.value === 'student') { filters.value.studentId = ''; filters.value.studentSort = '' }
  else if (activeFilter.value === 'marks')  { filters.value.minMarks = null; filters.value.marksSort = '' }
  else if (activeFilter.value === 'status') { filters.value.status = '' }
}

const toggleKeyLog = (attempt) => {
  const was = attempt._showKeys
  attempts.value.forEach(a => { a._showKeys = false })
  attempt._showKeys = !was
}

const handleClickOutside = (e) => {
  if (!e.target.closest('.filter-popup')) activeFilter.value = null
}

onMounted(()        => { fetchAttempts(); document.addEventListener('click', handleClickOutside) })
onBeforeUnmount(()  => { document.removeEventListener('click', handleClickOutside) })

const filteredAttempts = computed(() => {
  let r = attempts.value.filter(a => {
    if (filters.value.studentId && !String(a.Applicant_Id).includes(filters.value.studentId)) return false
    if (filters.value.minMarks  !== null && a.Marks_Obtained < filters.value.minMarks)        return false
    if (filters.value.status    && a.Status !== filters.value.status)                         return false
    return true
  })
  if (filters.value.studentSort === 'asc')  r = [...r].sort((a,b) => a.Applicant_Id - b.Applicant_Id)
  if (filters.value.studentSort === 'desc') r = [...r].sort((a,b) => b.Applicant_Id - a.Applicant_Id)
  if (filters.value.marksSort   === 'asc')  r = [...r].sort((a,b) => a.Marks_Obtained - b.Marks_Obtained)
  if (filters.value.marksSort   === 'desc') r = [...r].sort((a,b) => b.Marks_Obtained - a.Marks_Obtained)
  return r
})

const totalPages      = computed(() => Math.ceil(filteredAttempts.value.length / itemsPerPage.value))
const paginatedAttempts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  return filteredAttempts.value.slice(start, start + itemsPerPage.value)
})

// ─── MAIN FETCH ──────────────────────────────────────────────────────────────
const fetchAttempts = async () => {
  try {
    const email = localStorage.getItem('email')
    const role  = localStorage.getItem('active_role')

    // ✅ Hits exam_result_routes.py  GET /api/attempts  (includes key logs)
    const res = await axios.get(`${API_BASE}/attempts`, {
      params: { exam_id: examId.value, email, role }
    })

    if (!res.data.success) { error.value = 'Unauthorized'; return }

    // Debug: check browser console to verify key_log_total is in the response
    console.log('✅ Attempts received:', res.data.attempts.length)
    if (res.data.attempts.length > 0) {
      console.log('🔑 Sample key_log_total:', res.data.attempts[0].key_log_total)
      console.log('🔑 Sample key_log_summary:', res.data.attempts[0].key_log_summary)
    }

    attempts.value = res.data.attempts.map(a => ({ ...a, _showKeys: false }))
  } catch (err) {
    console.error('❌ fetchAttempts error:', err.response?.data || err.message)
    error.value = 'Something went wrong.'
  }
}

const viewAnswers = (id) => router.push({ name: 'ViewAnswers', params: { attemptId: id } })

const goBack = () => {
  const role = localStorage.getItem('active_role')
  if (role === 'Admin')        router.push('/admin/exams')
  else if (role === 'Faculty') router.push('/faculty')
  else                         router.push('/')
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: all .2s }
.fade-enter-from, .fade-leave-to       { opacity: 0; transform: translateY(-6px) }
</style>