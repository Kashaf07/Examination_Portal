<template>
  <div
    v-if="!error"
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

      <!-- Title + Buttons -->
      <div class="flex items-center justify-between mb-6">
        <h1
          class="text-3xl font-bold tracking-tight
                 bg-gradient-to-r from-blue-600 to-purple-700
                 bg-clip-text text-transparent inline-block"
        >
          Student Attempts for Exam {{ examId }}
        </h1>

        <div class="flex gap-4">
          <button
            @click="goToResult"
            class="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition hover:scale-105"
          >
            Result
          </button>

          <button
            @click="goToAnalytics"
            class="bg-purple-500 hover:bg-purple-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition hover:scale-105"
          >
            Analytics
          </button>
        </div>
      </div>

      <!-- TABLE -->
      <div class="rounded-xl shadow-xl overflow-x-auto bg-white w-full">
        <table class="w-full border-separate border-spacing-0 min-w-[900px]">
          <thead>
            <tr class="bg-gradient-to-r from-blue-200 to-purple-200 text-blue-900 font-bold">

              <th class="px-6 py-4 text-left">Attempt ID</th>

              <!-- STUDENT FILTER -->
              <th class="px-6 py-4 text-left">
                <div class="flex items-center gap-2">
                  Student ID
                  <svg
                    @click.stop="openFilter($event, 'student')"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                    class="w-5 h-5 cursor-pointer transition"
                    :class="filters.studentId || filters.studentSort
                      ? 'text-blue-600'
                      : 'text-gray-500 hover:text-blue-600'"
                  >
                    <path d="M3 4h18l-7 8v6l-4 2v-8L3 4z"/>
                  </svg>
                </div>
              </th>

              <th class="px-6 py-4 text-left">Student Email</th>
              <th class="px-6 py-4 text-left">Start Time</th>
              <th class="px-6 py-4 text-left">End Time</th>

              <!-- MARKS FILTER -->
              <th class="px-6 py-4 text-right">
                <div class="flex items-center justify-end gap-2">
                  Marks
                  <svg
                    @click.stop="openFilter($event, 'marks')"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                    class="w-5 h-5 cursor-pointer transition"
                    :class="filters.minMarks !== null || filters.marksSort
                      ? 'text-blue-600'
                      : 'text-gray-500 hover:text-blue-600'"
                  >
                    <path d="M3 4h18l-7 8v6l-4 2v-8L3 4z"/>
                  </svg>
                </div>
              </th>

              <th class="px-6 py-4 text-right">Max Marks</th>

              <!-- STATUS FILTER -->
              <th class="px-6 py-4 text-center">
                <div class="flex items-center justify-center gap-2">
                  Status
                  <svg
                    @click.stop="openFilter($event, 'status')"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                    class="w-5 h-5 cursor-pointer transition"
                    :class="filters.status
                      ? 'text-blue-600'
                      : 'text-gray-500 hover:text-blue-600'"
                  >
                    <path d="M3 4h18l-7 8v6l-4 2v-8L3 4z"/>
                  </svg>
                </div>
              </th>

              <th class="px-6 py-4 text-center">Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="attempt in filteredAttempts"
              :key="attempt.Attempt_Id"
              class="hover:bg-blue-50 border-b border-gray-100"
            >
              <td class="px-6 py-3">{{ attempt.Attempt_Id }}</td>
              <td class="px-6 py-3">{{ attempt.Applicant_Id }}</td>
              <td class="px-6 py-3">{{ attempt.Student_Email || '-' }}</td>
              <td class="px-6 py-3">{{ attempt.Start_Time }}</td>
              <td class="px-6 py-3">{{ attempt.End_Time || '-' }}</td>
              <td class="px-6 py-3 text-right">{{ attempt.Marks_Obtained }}</td>
              <td class="px-6 py-3 text-right">{{ attempt.Max_Marks }}</td>
              <td class="px-6 py-3 text-center">
                <span
                  :class="{
                    'text-green-600 font-semibold': attempt.Status === 'Pass',
                    'text-red-500 font-semibold': attempt.Status === 'Fail'
                  }"
                >
                  {{ attempt.Status }}
                </span>
              </td>
              <td class="px-6 py-3 text-center">
                <button
                  @click="viewAnswers(attempt.Attempt_Id)"
                  class="bg-purple-600 hover:bg-purple-700 text-white px-5 py-2 rounded-full font-semibold shadow"
                >
                  View Answers
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
  </div>
   <!-- UNAUTHORIZED UI -->
  <div
    v-else
    class="min-h-screen flex items-center justify-center bg-red-50"
  >
    <div class="bg-white shadow-xl rounded-xl p-8 text-center">
      <h2 class="text-2xl font-bold text-red-600 mb-4">
        Unauthorized Access
      </h2>
      <p class="text-gray-600">
        You are not allowed to access this exam.
      </p>
    </div>
  </div>

  <!-- FILTER POPOVER -->
  <transition name="fade">
    <div
      v-if="activeFilter"
      :style="popoverStyle"
      class="fixed bg-white shadow-2xl border border-gray-200
             rounded-xl p-4 w-72 z-[9999] max-w-[95vw]"
    >

      <!-- STUDENT FILTER -->
      <div v-if="activeFilter === 'student'">
        <input
          v-model="filters.studentId"
          type="text"
          placeholder="Search Student ID..."
          class="w-full border px-3 py-2 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none mb-3"
        />

        <label class="text-xs text-gray-500 font-semibold block mb-2">
          Sort Student ID
        </label>

        <div class="flex justify-center gap-8 text-2xl font-bold">
          <span
            @click="toggleStudentSort('asc')"
            :class="filters.studentSort === 'asc'
              ? 'text-blue-600 cursor-pointer'
              : 'text-gray-400 hover:text-blue-600 cursor-pointer'"
          >↑</span>

          <span
            @click="toggleStudentSort('desc')"
            :class="filters.studentSort === 'desc'
              ? 'text-blue-600 cursor-pointer'
              : 'text-gray-400 hover:text-blue-600 cursor-pointer'"
          >↓</span>
        </div>
      </div>

      <!-- MARKS FILTER -->
      <div v-if="activeFilter === 'marks'">
        <label class="text-xs text-gray-500 font-semibold block mb-2">
          Minimum Marks
        </label>

        <input
          v-model.number="filters.minMarks"
          type="number"
          placeholder="Minimum Marks..."
          class="w-full border px-3 py-2 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none mb-4"
        />

        <label class="text-xs text-gray-500 font-semibold block mb-2">
          Sort Marks
        </label>

        <div class="flex justify-center gap-8 text-2xl font-bold">
          <span
            @click="toggleMarksSort('asc')"
            :class="filters.marksSort === 'asc'
              ? 'text-blue-600 cursor-pointer'
              : 'text-gray-400 hover:text-blue-600 cursor-pointer'"
          >↑</span>

          <span
            @click="toggleMarksSort('desc')"
            :class="filters.marksSort === 'desc'
              ? 'text-blue-600 cursor-pointer'
              : 'text-gray-400 hover:text-blue-600 cursor-pointer'"
          >↓</span>
        </div>
      </div>

      <!-- STATUS FILTER -->
<div v-if="activeFilter === 'status'">

  <label class="text-xs text-gray-500 font-semibold block mb-3">
    Filter by Status
  </label>

  <div class="flex gap-3 flex-wrap">

    <!-- PASS -->
    <button
      @click="filters.status = filters.status === 'Pass' ? '' : 'Pass'"
      class="flex-1 min-w-[90px] px-4 py-2 rounded-lg border font-semibold transition text-center"
      :class="filters.status === 'Pass'
        ? 'bg-green-600 text-white border-green-600'
        : 'bg-white text-green-600 border-green-400 hover:bg-green-50'"
    >
      Pass
    </button>

    <!-- FAIL -->
    <button
      @click="filters.status = filters.status === 'Fail' ? '' : 'Fail'"
      class="flex-1 min-w-[90px] px-4 py-2 rounded-lg border font-semibold transition text-center"
      :class="filters.status === 'Fail'
        ? 'bg-red-600 text-white border-red-600'
        : 'bg-white text-red-600 border-red-400 hover:bg-red-50'"
    >
      Fail
    </button>

    <!-- RESTRICTED -->
    <button
      @click="filters.status = filters.status === 'Restricted' ? '' : 'Restricted'"
      class="flex-1 min-w-[90px] px-4 py-2 rounded-lg border font-semibold transition text-center"
      :class="filters.status === 'Restricted'
        ? 'bg-amber-500 text-white border-amber-500'
        : 'bg-white text-amber-600 border-amber-500 hover:bg-amber-50'"
    >
      Restricted
    </button>

  </div>

</div>

      <div class="flex justify-between mt-4">
        <button @click="applyFilter" class="text-sm text-blue-600 font-semibold">
          Apply
        </button>
        <button @click="clearCurrentFilter" class="text-sm text-red-500 font-semibold">
          Clear
        </button>
      </div>

    </div>
       
  </transition>

  
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

const activeFilter = ref(null)
const popoverStyle = ref({})

const filters = ref({
  studentId: '',
  minMarks: null,
  status: '',
  marksSort: '',
  studentSort: ''
})

/* SMART OVERFLOW FIX */
const openFilter = (event, type) => {
  activeFilter.value = type

  const rect = event.target.getBoundingClientRect()
  const popupWidth = 288
  const padding = 16

  let left = rect.left
  let top = rect.bottom + 8

  if (left + popupWidth > window.innerWidth - padding) {
    left = window.innerWidth - popupWidth - padding
  }

  if (left < padding) {
    left = padding
  }

  popoverStyle.value = {
    top: `${top}px`,
    left: `${left}px`
  }
}

const toggleStudentSort = (direction) => {
  filters.value.studentSort =
    filters.value.studentSort === direction ? '' : direction
  filters.value.marksSort = ''
}

const toggleMarksSort = (direction) => {
  filters.value.marksSort =
    filters.value.marksSort === direction ? '' : direction
  filters.value.studentSort = ''
}

const clearCurrentFilter = () => {
  if (activeFilter.value === 'student') {
    filters.value.studentId = ''
    filters.value.studentSort = ''
  }
  if (activeFilter.value === 'marks') {
    filters.value.minMarks = null
    filters.value.marksSort = ''
  }
  if (activeFilter.value === 'status') {
    filters.value.status = ''
  }
}

const applyFilter = () => activeFilter.value = null

const handleClickOutside = (e) => {
  if (!e.target.closest('.fixed')) activeFilter.value = null
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  fetchAttempts()
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

const filteredAttempts = computed(() => {
  let result = attempts.value.filter(a => {
    if (filters.value.studentId &&
        !String(a.Applicant_Id).includes(filters.value.studentId)) return false
    if (filters.value.minMarks !== null &&
        a.Marks_Obtained < filters.value.minMarks) return false
    if (filters.value.status &&
        a.Status !== filters.value.status) return false
    return true
  })

  if (filters.value.studentSort === 'asc')
    result.sort((a,b)=>a.Applicant_Id-b.Applicant_Id)
  if (filters.value.studentSort === 'desc')
    result.sort((a,b)=>b.Applicant_Id-a.Applicant_Id)
  if (filters.value.marksSort === 'asc')
    result.sort((a,b)=>a.Marks_Obtained-b.Marks_Obtained)
  if (filters.value.marksSort === 'desc')
    result.sort((a,b)=>b.Marks_Obtained-a.Marks_Obtained)

  return result
})

const fetchAttempts = async () => {
  try {
    const email = localStorage.getItem("email")
    const role = localStorage.getItem("active_role")
    const res = await axios.get('/attempts', {
      params: { exam_id: examId.value, email, role }
    })
    if (!res.data.success) {
      error.value = "Unauthorized Access"
      return
    }
    attempts.value = res.data.attempts
  } catch {
    error.value = "Unauthorized Access"
  }
}

const viewAnswers = (attemptId) => {
  router.push({ name: 'ViewAnswers', params: { attemptId } })
}

const goToResult = () => {
  router.push(`/exam/${examId.value}/result`)
}

const goToAnalytics = () => {
  router.push({ name: 'ExamAnalytics', params: { examId: examId.value } })
}

const goBack = () => {
  const role = localStorage.getItem('active_role')
  if (role === 'Admin') router.push('/admin/exams')
  else if (role === 'Faculty') router.push('/faculty')
  else router.push('/')
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.18s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>