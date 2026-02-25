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
        ← Back
      </button>

      <!-- Title + Actions Row -->
      <div class="flex items-center justify-between mb-6">

      <h1
          class="text-3xl font-bold tracking-tight 
                bg-gradient-to-r from-blue-600 to-purple-700 
                bg-clip-text text-transparent inline-block"
        >
          Student Attempts for Exam {{ examId }}
        </h1>

        <!-- Action Buttons -->
        <div class="flex gap-4">

          <!-- Result Button -->
          <button
            @click="goToResult"
            class="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all duration-200 hover:scale-105"
          >
            Result
          </button>

          <!-- Analytics Button -->
          <button
            @click="goToAnalytics"
            class="bg-purple-500 hover:bg-purple-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all duration-200 hover:scale-105"
          >
            Analytics
          </button>

        </div>

      </div>

           <!-- TABLE CARD -->

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
                    :class="filters.studentId ? 'text-blue-600' : 'text-gray-500 hover:text-blue-600'"
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
                    :class="filters.minMarks !== null ? 'text-blue-600' : 'text-gray-500 hover:text-blue-600'"
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
                    :class="filters.status ? 'text-blue-600' : 'text-gray-500 hover:text-blue-600'"
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
              v-for="attempt in paginatedAttempts"
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

            <tr v-if="filteredAttempts.length === 0">
              <td colspan="9" class="text-center py-8 text-gray-500 italic">
                No matching attempts found.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- FLOATING FILTER -->
  <transition name="fade">
    <div
      v-if="activeFilter"
      :style="popoverStyle"
      class="fixed bg-white shadow-2xl border border-gray-200 
             rounded-xl p-4 w-72 z-[9999]"
    >
      <div v-if="activeFilter === 'student'">
        <input
          v-model="filters.studentId"
          type="text"
          placeholder="Search Student ID..."
          class="w-full border px-3 py-2 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none"
        />
      </div>

      <div v-if="activeFilter === 'marks'">

  <!-- SORT OPTION -->
  <label class="text-xs text-gray-500 font-semibold block mb-2">
    Sort Marks
  </label>

  <select
    v-model="filters.marksSort"
    class="w-full border px-3 py-2 rounded-lg mb-3 
           focus:ring-2 focus:ring-blue-400 outline-none"
  >
    <option value="">None</option>
    <option value="asc">Low to High</option>
    <option value="desc">High to Low</option>
  </select>

  <!-- MIN MARKS -->
  <label class="text-xs text-gray-500 font-semibold block mb-2">
    Minimum Marks
  </label>

  <input
    v-model.number="filters.minMarks"
    type="number"
    placeholder="Minimum Marks..."
    class="w-full border px-3 py-2 rounded-lg 
           focus:ring-2 focus:ring-blue-400 outline-none"
  />
</div>

      <div v-if="activeFilter === 'status'">
        <select
          v-model="filters.status"
          class="w-full border px-3 py-2 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none"
        >
          <option value="">All</option>
          <option value="Pass">Pass</option>
          <option value="Fail">Fail</option>
        </select>
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

const goToResult = () => {
  console.log("Navigating to:", `/exam/${examId.value}/result`)
  router.push(`/exam/${examId.value}/result`)
}

const goToAnalytics = () => {
  router.push({
    name: 'ExamAnalytics',
    params: { examId: examId.value }
  })
}

// ================= PAGINATION STATE =================
const currentPage = ref(1)
const itemsPerPage = ref(15)

// ================= PAGINATION COMPUTED =================
const totalAttempts = computed(() => attempts.value.length)
const totalPages = computed(() => Math.ceil(totalAttempts.value / itemsPerPage.value))
const activeFilter = ref(null)
const popoverStyle = ref({})

const filters = ref({
  studentId: '',
  minMarks: null,
  status: '',
  marksSort: '' // NEW
})

const openFilter = (event, type) => {
  activeFilter.value = type
  const rect = event.target.getBoundingClientRect()

  popoverStyle.value = {
    top: rect.bottom + 8 + 'px',
    left: rect.left + 'px'
  }
}

const clearCurrentFilter = () => {
  if (activeFilter.value === 'student') {
    filters.value.studentId = ''
  }

  if (activeFilter.value === 'marks') {
    filters.value.minMarks = null
    filters.value.marksSort = ''
  }

  if (activeFilter.value === 'status') {
    filters.value.status = ''
  }
}

const applyFilter = () => {
  activeFilter.value = null
}

const handleClickOutside = (e) => {
  if (!e.target.closest('.fixed')) {
    activeFilter.value = null
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

const filteredAttempts = computed(() => {
  let result = attempts.value.filter(a => {

    if (filters.value.studentId &&
        !String(a.Applicant_Id).includes(filters.value.studentId))
      return false

    if (filters.value.minMarks !== null &&
        a.Marks_Obtained < filters.value.minMarks)
      return false

    if (filters.value.status &&
        a.Status !== filters.value.status)
      return false

    return true
  })

  // SORTING LOGIC
  if (filters.value.marksSort === 'asc') {
    result.sort((a, b) => a.Marks_Obtained - b.Marks_Obtained)
  }

  if (filters.value.marksSort === 'desc') {
    result.sort((a, b) => b.Marks_Obtained - a.Marks_Obtained)
  }

  return result
})

const paginatedAttempts = computed(() => filteredAttempts.value)

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

const goBack = () => {
  const role = localStorage.getItem('active_role')
  if (role === 'Admin') router.push('/admin/exams')
  else if (role === 'Faculty') router.push('/faculty')
  else router.push('/')
}

onMounted(fetchAttempts)
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