<template>
  <div v-if="!error" class="min-h-screen w-full bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 flex flex-col items-center py-10">
    <div class="w-full max-w-full px-6">
      <button @click="goBack" class="mb-6 flex items-center gap-2 px-4 py-2 bg-white/70 hover:bg-white/90 text-gray-800 rounded-lg shadow-md hover:shadow-lg transition-all duration-200 backdrop-blur-sm border border-gray-200">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
        </svg>
        <span class="font-semibold">Back</span>
      </button>
      <div class="flex items-center justify-between mb-6">
        <h1 class="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-700 tracking-tight">Student Attempts for Exam {{ examId }}</h1>
        <div class="flex gap-4">
          <button @click="goToResult" class="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all duration-200 hover:scale-105">Result</button>
          <button @click="goToAnalytics" class="bg-purple-500 hover:bg-purple-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all duration-200 hover:scale-105">Analytics</button>
        </div>
      </div>
      <div class="rounded-xl shadow-xl overflow-x-auto bg-white w-full">
        <table class="w-full border-separate border-spacing-0 min-w-[980px]">
          <thead>
            <tr class="bg-gradient-to-r from-blue-200 to-purple-200 text-blue-900 font-bold text-sm">
              <th class="px-4 py-3 text-left">Attempt ID</th>
              <th class="px-4 py-3 text-left">
                <div class="flex items-center gap-2">Student ID
                  <svg @click.stop="openFilter($event,'student')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5 cursor-pointer" :class="filters.studentId || filters.studentSort ? 'text-blue-600' : 'text-gray-500 hover:text-blue-600'"><path d="M3 4h18l-7 8v6l-4 2v-8L3 4z"/></svg>
                </div>
              </th>
              <th class="px-4 py-3 text-left">Student Email</th>
              <th class="px-4 py-3 text-left">Start Time</th>
              <th class="px-4 py-3 text-left">End Time</th>
              <th class="px-4 py-3 text-center">
                <div class="flex items-center justify-center gap-2">Marks Obtained
                  <svg @click.stop="openFilter($event,'marks')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5 cursor-pointer" :class="filters.minMarks !== null || filters.marksSort ? 'text-blue-600' : 'text-gray-500 hover:text-blue-600'"><path d="M3 4h18l-7 8v6l-4 2v-8L3 4z"/></svg>
                </div>
              </th>
              <th class="px-4 py-3 text-center">Max Marks</th>
              <th class="px-4 py-3 text-center">
                <div class="flex items-center justify-center gap-2">Status
                  <svg @click.stop="openFilter($event,'status')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5 cursor-pointer" :class="filters.status ? 'text-blue-600' : 'text-gray-500 hover:text-blue-600'"><path d="M3 4h18l-7 8v6l-4 2v-8L3 4z"/></svg>
                </div>
              </th>
              <th class="px-4 py-3 text-center">Key Activity</th>
              <th class="px-4 py-3 text-center">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="attempt in paginatedAttempts" :key="attempt.Attempt_Id" class="hover:bg-blue-50 border-b border-gray-100 text-sm">
              <td class="px-4 py-2.5">{{ attempt.Attempt_Id }}</td>
              <td class="px-4 py-2.5">{{ attempt.Applicant_Id }}</td>
              <td class="px-4 py-2.5 break-words">{{ attempt.Student_Email || '-' }}</td>
              <td class="px-4 py-2.5">
                <div class="flex flex-col leading-tight">
                  <span>{{ attempt.Start_Date }}</span>
                  <span class="text-gray-600">{{ attempt.Start_Time_Only }}</span>
                </div>
              </td>
              <td class="px-4 py-2.5">
                <div v-if="attempt.End_Date" class="flex flex-col leading-tight">
                  <span>{{ attempt.End_Date }}</span>
                  <span class="text-gray-600">{{ attempt.End_Time_Only }}</span>
                </div>
                <span v-else>-</span>
              </td>
              <td class="px-4 py-2.5 text-center">{{ attempt.Marks_Obtained }}</td>
              <td class="px-4 py-2.5 text-center">{{ attempt.Max_Marks }}</td>
              <td class="px-4 py-2.5 text-center">
                <span :class="{'text-green-600 font-semibold': attempt.Status === 'Pass','text-red-500 font-semibold': attempt.Status === 'Fail','text-black font-semibold': attempt.Status === 'Restricted'}">{{ attempt.Status || '-' }}</span>
              </td>
              <td class="px-4 py-2.5 text-center">
                <div v-if="!attempt.key_log_total || attempt.key_log_total === 0" class="text-gray-400 text-sm italic">None</div>
                <div v-else class="relative flex flex-col items-center">
                  <button @click.stop="toggleKeyLog(attempt.Attempt_Id, $event)"
                    class="inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-semibold border transition-all duration-200"
                    :class="attempt._showKeys ? 'bg-indigo-600 text-white border-indigo-600 shadow-md' : 'bg-white text-indigo-600 border-indigo-300 hover:bg-indigo-50'">
                    🔑 {{ attempt.key_log_total }}
                    <svg class="w-3 h-3 transition-transform duration-200" :class="attempt._showKeys ? 'rotate-180' : ''" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
                    </svg>
                  </button>
                </div>
              </td>
              <td class="px-4 py-2.5 text-center">
                <button @click="viewAnswers(attempt.Attempt_Id)" class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-full text-sm font-semibold shadow">View Answers</button>
              </td>
            </tr>
            <tr v-if="filteredAttempts.length === 0">
              <td colspan="10" class="text-center py-8 text-gray-500 italic">No matching attempts found.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- KEY LOG DROPDOWN - OUTSIDE TABLE -->
      <div v-for="attempt in paginatedAttempts" :key="'dropdown-' + attempt.Attempt_Id">
        <div v-if="attempt._showKeys" class="fixed z-[9999] bg-white border border-gray-200 rounded-xl shadow-2xl p-4 min-w-[300px] max-w-[400px]" :style="dropdownPositions[attempt.Attempt_Id] || {}">
          <div class="text-xs font-bold text-gray-500 mb-3 uppercase tracking-wide">Key Log Summary</div>
          <div class="max-h-[350px] overflow-y-auto pr-2 custom-scrollbar">
            <div v-for="(s, i) in attempt.key_log_summary" :key="i" class="flex items-center justify-between gap-3 py-2 border-b border-gray-50 last:border-0">
              <span class="flex items-center gap-2 text-sm">
                <span v-if="s.event_type === 'blocked'" class="text-red-500 text-lg">🚫</span>
                <span v-else-if="s.event_type === 'warning'" class="text-amber-500 text-lg">⚠️</span>
                <span v-else class="text-green-500 text-lg">✅</span>
                <span class="font-medium text-gray-700">{{ s.key_label }}</span>
              </span>
              <span class="text-xs font-bold text-gray-400 ml-2">×{{ s.count }}</span>
            </div>
          </div>
          <div class="mt-3 pt-3 border-t border-gray-100 flex justify-between text-xs text-gray-400">
            <span>Total violations</span>
            <span class="font-bold text-gray-600">{{ attempt.key_log_total }}</span>
          </div>
        </div>
      </div>

      <div v-if="totalPages > 1" class="flex justify-center items-center gap-3 mt-6">
        <button @click="currentPage--" :disabled="currentPage === 1" class="px-4 py-2 rounded-lg bg-white border border-gray-300 text-gray-700 font-semibold shadow hover:bg-blue-50 disabled:opacity-40 disabled:cursor-not-allowed transition">← Prev</button>
        <span class="text-gray-600 font-medium">Page {{ currentPage }} of {{ totalPages }}</span>
        <button @click="currentPage++" :disabled="currentPage === totalPages" class="px-4 py-2 rounded-lg bg-white border border-gray-300 text-gray-700 font-semibold shadow hover:bg-blue-50 disabled:opacity-40 disabled:cursor-not-allowed transition">Next →</button>
      </div>
    </div>
  </div>

  <transition name="fade">
    <div v-if="activeFilter" :style="popoverStyle" class="filter-popup fixed bg-white shadow-2xl border border-gray-200 rounded-xl p-4 w-72 z-[9999] max-w-[95vw]">
      <div v-if="activeFilter === 'student'">
        <input v-model="filters.studentId" placeholder="Search Student ID" class="w-full border px-3 py-2 rounded-lg mb-3"/>
        <div class="flex justify-center gap-8 text-2xl font-bold">
          <span @click="toggleStudentSort('asc')" :class="filters.studentSort==='asc'?'text-blue-600 cursor-pointer':'text-gray-400 cursor-pointer'">↑</span>
          <span @click="toggleStudentSort('desc')" :class="filters.studentSort==='desc'?'text-blue-600 cursor-pointer':'text-gray-400 cursor-pointer'">↓</span>
        </div>
      </div>
      <div v-if="activeFilter === 'marks'">
        <input v-model.number="filters.minMarks" type="number" placeholder="Minimum Marks" class="w-full border px-3 py-2 rounded-lg mb-3"/>
        <div class="flex justify-center gap-8 text-2xl font-bold">
          <span @click="toggleMarksSort('asc')" :class="filters.marksSort==='asc'?'text-blue-600 cursor-pointer':'text-gray-400 cursor-pointer'">↑</span>
          <span @click="toggleMarksSort('desc')" :class="filters.marksSort==='desc'?'text-blue-600 cursor-pointer':'text-gray-400 cursor-pointer'">↓</span>
        </div>
      </div>
      <div v-if="activeFilter === 'status'">
        <label class="text-xs text-gray-500 font-semibold block mb-3">Filter by Status</label>
        <div class="flex gap-3 flex-wrap">
          <button @click="filters.status = filters.status === 'Pass' ? '' : 'Pass'" class="flex-1 min-w-[90px] px-4 py-2 rounded-lg border font-semibold transition text-center" :class="filters.status === 'Pass' ? 'bg-green-600 text-white border-green-600' : 'bg-white text-green-600 border-green-400 hover:bg-green-50'">Pass</button>
          <button @click="filters.status = filters.status === 'Fail' ? '' : 'Fail'" class="flex-1 min-w-[90px] px-4 py-2 rounded-lg border font-semibold transition text-center" :class="filters.status === 'Fail' ? 'bg-red-600 text-white border-red-600' : 'bg-white text-red-600 border-red-400 hover:bg-red-50'">Fail</button>
          <button @click="filters.status = filters.status === 'Restricted' ? '' : 'Restricted'" class="flex-1 min-w-[90px] px-4 py-2 rounded-lg border font-semibold transition text-center" :class="filters.status === 'Restricted' ? 'bg-amber-500 text-white border-amber-500' : 'bg-white text-amber-600 border-amber-500 hover:bg-amber-50'">Restricted</button>
        </div>
      </div>
      <div class="flex justify-between mt-4">
        <button @click="applyFilter" class="text-blue-600 font-semibold">Apply</button>
        <button @click="clearCurrentFilter" class="text-red-500 font-semibold">Clear</button>
      </div>
    </div>
  </transition>

  <div v-if="error" class="min-h-screen flex items-center justify-center bg-red-50">
    <div class="bg-white shadow-xl rounded-xl p-8 text-center">
      <h2 class="text-2xl font-bold text-red-600 mb-4">Unauthorized Access</h2>
      <p class="text-gray-600 mb-6">You are not allowed to access this exam.</p>
      <button @click="router.back()" class="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-lg font-semibold shadow-md transition">Go Back</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from '../utils/axiosInstance'

const route = useRoute()
const router = useRouter()
const examId = ref(route.params.examId)
const attempts = ref([])
const error = ref('')
const currentPage = ref(1)
const itemsPerPage = ref(15)
const activeFilter = ref(null)
const popoverStyle = ref({})
const dropdownPositions = ref({})
const filters = ref({ studentId: '', minMarks: null, status: '', marksSort: '', studentSort: '' })

const goToResult    = () => router.push({ name: 'ExamResult',    params: { examId: examId.value } })
const goToAnalytics = () => router.push({ name: 'ExamAnalytics', params: { examId: examId.value } })

// ✅ KEY FIX: Replace the whole object in the array so Vue 3 reactive system
// detects the change. Direct mutation `attempt._showKeys = x` is NOT tracked
// by Vue 3 on plain objects inside a ref([]) array.
const toggleKeyLog = (attemptId, event) => {
  // Store button position for this attempt
  if (event?.target) {
    const button = event.target.closest('button')
    if (button) {
      const rect = button.getBoundingClientRect()
      dropdownPositions.value[attemptId] = {
        top: `${rect.bottom + window.scrollY + 8}px`,
        left: `${rect.left + window.scrollX}px`
      }
    }
  }
  
  attempts.value = attempts.value.map(a => {
    if (a.Attempt_Id === attemptId) return { ...a, _showKeys: !a._showKeys }
    return a._showKeys ? { ...a, _showKeys: false } : a
  })
}

const openFilter = (event, type) => {
  activeFilter.value = type
  const rect = event.target.getBoundingClientRect()
  const popupWidth = 288, padding = 16
  let left = rect.left, top = rect.bottom + 8
  if (left + popupWidth > window.innerWidth - padding) left = window.innerWidth - popupWidth - padding
  if (left < padding) left = padding
  popoverStyle.value = { top: `${top}px`, left: `${left}px` }
}

const toggleStudentSort = (dir) => { filters.value.studentSort = filters.value.studentSort === dir ? '' : dir }
const toggleMarksSort   = (dir) => { filters.value.marksSort   = filters.value.marksSort   === dir ? '' : dir }
const applyFilter = () => { currentPage.value = 1; activeFilter.value = null }
const clearCurrentFilter = () => { filters.value = { studentId: '', minMarks: null, status: '', marksSort: '', studentSort: '' } }
const handleClickOutside = (e) => { if (!e.target.closest('.filter-popup')) activeFilter.value = null }

onMounted(() => { fetchAttempts(); document.addEventListener('click', handleClickOutside) })
onBeforeUnmount(() => { document.removeEventListener('click', handleClickOutside) })

const filteredAttempts = computed(() => {
  let result = attempts.value.filter(a => {
    if (filters.value.studentId && !String(a.Applicant_Id).includes(filters.value.studentId)) return false
    if (filters.value.minMarks !== null && a.Marks_Obtained < filters.value.minMarks) return false
    if (filters.value.status && a.Status !== filters.value.status) return false
    return true
  })
  if (filters.value.studentSort === 'asc')  result.sort((a, b) => String(a.Applicant_Id).localeCompare(String(b.Applicant_Id)))
  if (filters.value.studentSort === 'desc') result.sort((a, b) => String(b.Applicant_Id).localeCompare(String(a.Applicant_Id)))
  if (filters.value.marksSort   === 'asc')  result.sort((a, b) => a.Marks_Obtained - b.Marks_Obtained)
  if (filters.value.marksSort   === 'desc') result.sort((a, b) => b.Marks_Obtained - a.Marks_Obtained)
  return result
})

const totalPages = computed(() => Math.ceil(filteredAttempts.value.length / itemsPerPage.value))
const paginatedAttempts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  return filteredAttempts.value.slice(start, start + itemsPerPage.value)
})

const fetchAttempts = async () => {
  try {
    const email = localStorage.getItem('email')
    const role  = localStorage.getItem('active_role')
    const res = await axios.get('/attempts', { params: { exam_id: examId.value, email, role } })
    if (!res.data.success) { router.replace('/admin/exams'); return }
    
    // Format dates: separate date and time for two-line display
    attempts.value = res.data.attempts.map(a => {
      const formatDateTime = (dateStr) => {
        if (!dateStr) return { date: null, time: null }
        const date = new Date(dateStr)
        const day = String(date.getDate()).padStart(2, '0')
        const month = String(date.getMonth() + 1).padStart(2, '0')
        const year = date.getFullYear()
        const hours = String(date.getHours()).padStart(2, '0')
        const minutes = String(date.getMinutes()).padStart(2, '0')
        return {
          date: `${day}/${month}/${year}`,
          time: `${hours}:${minutes}`
        }
      }
      
      const startDT = formatDateTime(a.Start_Time)
      const endDT = formatDateTime(a.End_Time)
      
      return {
        ...a,
        Start_Date: startDT.date,
        Start_Time_Only: startDT.time,
        End_Date: endDT.date,
        End_Time_Only: endDT.time,
        _showKeys: false
      }
    })
  } catch { error.value = 'Something went wrong.' }
}

const viewAnswers = (id) => router.push({ name: 'ViewAnswers', params: { attemptId: id } })
const goBack = () => router.push('/admin/exams')
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: all .2s }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(-6px) }

/* Custom scrollbar for dropdown */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>