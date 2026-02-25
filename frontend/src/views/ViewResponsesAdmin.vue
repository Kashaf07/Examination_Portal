<template>
  <div
    v-if="!error"
    class="min-h-screen w-full bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 py-10"
  >
    <div class="w-full px-10">

      <!-- Back Button -->
      <button
        @click="goBack"
        class="mb-6 flex items-center gap-2 px-4 py-2 bg-white/80 hover:bg-white 
               text-gray-800 rounded-lg shadow-md hover:shadow-lg transition border border-gray-200"
      >
        ← Back
      </button>

      <h1
        class="text-3xl font-bold mb-8 text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-700"
      >
        Student Attempts for Exam {{ examId }}
      </h1>

      <div class="rounded-2xl shadow-xl bg-white w-full relative">

        <table class="w-full table-fixed border-separate border-spacing-0 text-sm">

          <!-- ================= HEADER ================= -->
          <thead>
            <tr class="bg-gradient-to-r from-blue-200 to-purple-200 text-blue-900 font-semibold">

              <th class="px-4 py-4 text-left w-[8%]">ID</th>

              <th class="px-6 py-4 text-left relative">
  <div class="flex items-center gap-2">
    Student ID

    <!-- FILTER ICON -->
    <svg
      @click="toggleFilter('student')"
      xmlns="http://www.w3.org/2000/svg"
      class="w-4 h-4 cursor-pointer"
      viewBox="0 0 24 24"
      fill="currentColor"
      :class="sortColumn === 'Applicant_Id' ? 'text-blue-600' : 'text-gray-500 hover:text-blue-600'"
    >
      <path d="M3 4h18l-7 8v6l-4 2v-8L3 4z"/>
    </svg>
  </div>

  <!-- SORT POPUP -->
  <div
  v-if="activeFilter === 'student'"
  class="absolute mt-1 bg-white border border-blue-300 
         rounded-md shadow-lg z-50 px-3 py-2 w-20"
>
  <div class="flex justify-center items-center gap-4">

    <!-- ASC -->
    <button
      @click="applySort('Applicant_Id','asc')"
      class="text-2xl font-black leading-none transition"
      :class="sortColumn === 'Applicant_Id' && sortDirection === 'asc'
        ? 'text-blue-700 scale-110'
        : 'text-gray-800 hover:text-blue-600'"
    >
      ↑
    </button>

    <!-- DESC -->
    <button
      @click="applySort('Applicant_Id','desc')"
      class="text-2xl font-black leading-none transition"
      :class="sortColumn === 'Applicant_Id' && sortDirection === 'desc'
        ? 'text-blue-700 scale-110'
        : 'text-gray-800 hover:text-blue-600'"
    >
      ↓
    </button>

  </div>
</div>
</th>
              <th class="px-4 py-4 text-left w-[18%]">Email</th>
              <th class="px-4 py-4 text-left w-[14%]">Start</th>
              <th class="px-4 py-4 text-left w-[14%]">End</th>

              <!-- MARKS WITH 2 ARROWS -->
              <th class="px-4 py-4 text-right w-[10%]">
                <div class="flex items-center justify-end gap-2">
                  Marks

                  <!-- ASC -->
                  <svg
                    @click.stop="applySort('Marks_Obtained','asc')"
                    class="w-4 h-4 cursor-pointer transition"
                    :class="sortColumn === 'Marks_Obtained' && sortDirection === 'asc'
                      ? 'text-blue-600'
                      : 'text-gray-400 hover:text-blue-600'"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path d="M5 12l5-5 5 5H5z"/>
                  </svg>

                  <!-- DESC -->
                  <svg
                    @click.stop="applySort('Marks_Obtained','desc')"
                    class="w-4 h-4 cursor-pointer transition"
                    :class="sortColumn === 'Marks_Obtained' && sortDirection === 'desc'
                      ? 'text-blue-600'
                      : 'text-gray-400 hover:text-blue-600'"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path d="M5 8l5 5 5-5H5z"/>
                  </svg>
                </div>
              </th>

              <th class="px-4 py-4 text-right w-[8%]">Max</th>

              <th class="px-4 py-4 text-center w-[8%]">Status</th>
              <th class="px-4 py-4 text-center w-[10%]">Actions</th>

            </tr>
          </thead>

          <!-- ================= BODY ================= -->
          <tbody>
            <tr v-for="attempt in paginatedAttempts"
                :key="attempt.Attempt_Id"
                class="hover:bg-blue-50 border-b border-gray-100 transition">

              <td class="px-4 py-3 truncate">{{ attempt.Attempt_Id }}</td>
              <td class="px-4 py-3 truncate">{{ attempt.Applicant_Id }}</td>
              <td class="px-4 py-3 break-words">{{ attempt.Student_Email || '-' }}</td>
              <td class="px-4 py-3 break-words">{{ attempt.Start_Time }}</td>
              <td class="px-4 py-3 break-words">{{ attempt.End_Time || '-' }}</td>
              <td class="px-4 py-3 text-right font-medium">{{ attempt.Marks_Obtained }}</td>
              <td class="px-4 py-3 text-right">{{ attempt.Max_Marks }}</td>

              <td class="px-4 py-3 text-center">
                <span :class="{
                  'text-green-600 font-semibold': attempt.Status === 'Pass',
                  'text-red-500 font-semibold': attempt.Status === 'Fail'
                }">
                  {{ attempt.Status }}
                </span>
              </td>

              <td class="px-4 py-3 text-center">
                <button
                  @click="viewAnswers(attempt.Attempt_Id)"
                  class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-full font-semibold shadow transition">
                  View
                </button>
              </td>

            </tr>

            <tr v-if="paginatedAttempts.length === 0">
              <td colspan="9" class="text-center py-8 text-gray-400 italic">
                No matching attempts found.
              </td>
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
import axios from '../utils/axiosInstance'

const route = useRoute()
const router = useRouter()

const examId = ref(route.params.examId)
const attempts = ref([])
const error = ref('')

const activeFilter = ref(null)
const sortColumn = ref('')
const sortDirection = ref('')
const statusFilter = ref(null)

const currentPage = ref(1)
const itemsPerPage = ref(15)

const applySort = (column, direction) => {
  if (sortColumn.value === column && sortDirection.value === direction) {
    sortColumn.value = ''
    sortDirection.value = ''
  } else {
    sortColumn.value = column
    sortDirection.value = direction
  }

  activeFilter.value = null
  currentPage.value = 1
}

const applyStatus = (status) => {
  statusFilter.value = status
  activeFilter.value = null
  currentPage.value = 1
}

const clearStatus = () => {
  statusFilter.value = null
}

const filteredAttempts = computed(() => {
  let result = [...attempts.value]

  if (statusFilter.value) {
    result = result.filter(a => a.Status === statusFilter.value)
  }

  if (sortColumn.value) {
    result.sort((a, b) => {
      let valA = a[sortColumn.value]
      let valB = b[sortColumn.value]

      if (sortColumn.value === 'Applicant_Id' || sortColumn.value === 'Marks_Obtained') {
        valA = Number(valA)
        valB = Number(valB)
      }

      if (sortDirection.value === 'asc') return valA > valB ? 1 : -1
      return valA < valB ? 1 : -1
    })
  }

  return result
})

const paginatedAttempts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  return filteredAttempts.value.slice(start, start + itemsPerPage.value)
})

const toggleFilter = (type) => {
  activeFilter.value = activeFilter.value === type ? null : type
}

const fetchAttempts = async () => {
  const email = localStorage.getItem("email")
  const role = localStorage.getItem("active_role")

  const res = await axios.get('/attempts', {
    params: { exam_id: examId.value, email, role }
  })

  attempts.value = res.data.attempts
}

const viewAnswers = (attemptId) => {
  router.push({ name: 'ViewAnswers', params: { attemptId } })
}

const goBack = () => {
  const role = localStorage.getItem('active_role')
  if (role === 'Admin') router.push('/admin/exams')
  else router.push('/faculty')
}

onMounted(fetchAttempts)
</script>