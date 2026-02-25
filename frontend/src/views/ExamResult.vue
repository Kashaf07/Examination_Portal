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
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5"
          viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd"
            d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z"
            clip-rule="evenodd" />
        </svg>
        <span class="font-semibold">Back</span>
      </button>

      <!-- Title + Download -->
      <div class="flex items-center justify-between mb-6">

        <h1
          class="text-3xl font-bold leading-relaxed
                 bg-gradient-to-r from-blue-600 to-purple-700 
                 bg-clip-text text-transparent inline-block"
        >
          {{ examName }} Result
        </h1>

        <button
          @click="downloadPDF"
          class="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all hover:scale-105"
        >
          Download Result
        </button>

      </div>

      <!-- Table -->
      <div class="rounded-xl shadow-xl overflow-x-auto bg-white w-full">
        <table class="w-full border-separate border-spacing-0 min-w-[900px]">
          <thead>
            <tr class="bg-gradient-to-r from-blue-200 to-purple-200 text-blue-900 font-bold">
              <th class="px-6 py-4 text-left">Student ID</th>
              <th class="px-6 py-4 text-left">Student Name</th>
              <th class="px-6 py-4 text-right">Marks</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="student in paginatedResults"
              :key="student.Applicant_Id"
              class="hover:bg-blue-50 transition-colors duration-200 border-b border-gray-100"
            >
              <td class="px-6 py-3">{{ student.Applicant_Id }}</td>
              <td class="px-6 py-3">{{ student.Student_Name }}</td>
              <td class="px-6 py-3 text-right">{{ student.Marks_Obtained }}</td>
            </tr>

            <tr v-if="results.length === 0">
              <td colspan="3" class="text-center py-8 text-gray-500 italic">
                No results available.
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination -->
        <div v-if="results.length > 20"
          class="bg-gray-50 px-6 py-4 border-t border-gray-200">

          <div class="flex items-center justify-between">

            <div class="text-sm text-gray-700">
              Showing 
              <span class="font-semibold">{{ startIndex + 1 }}</span>
              to 
              <span class="font-semibold">{{ endIndex }}</span>
              of 
              <span class="font-semibold">{{ totalResults }}</span>
              results
            </div>

            <div class="flex items-center gap-2">
              <button
                @click="goToPage(currentPage - 1)"
                :disabled="currentPage === 1"
                class="px-3 py-2 rounded-lg border border-gray-300 bg-white hover:bg-gray-50 disabled:opacity-50"
              >
                Prev
              </button>

              <button
                v-for="page in totalPages"
                :key="page"
                @click="goToPage(page)"
                class="px-4 py-2 rounded-lg border"
                :class="currentPage === page 
                  ? 'bg-blue-600 text-white border-blue-600' 
                  : 'border-gray-300 bg-white hover:bg-gray-50'"
              >
                {{ page }}
              </button>

              <button
                @click="goToPage(currentPage + 1)"
                :disabled="currentPage === totalPages"
                class="px-3 py-2 rounded-lg border border-gray-300 bg-white hover:bg-gray-50 disabled:opacity-50"
              >
                Next
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
import axios from '../utils/axiosInstance'
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'

const route = useRoute()
const router = useRouter()

const examId = route.params.examId
const results = ref([])
const examName = ref("Exam")
const examDate = ref("")
const examTime = ref("")

// Pagination
const currentPage = ref(1)
const itemsPerPage = 20

const totalResults = computed(() => results.value.length)
const totalPages = computed(() =>
  Math.ceil(totalResults.value / itemsPerPage)
)

const paginatedResults = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return results.value.slice(start, start + itemsPerPage)
})

const startIndex = computed(() =>
  (currentPage.value - 1) * itemsPerPage
)

const endIndex = computed(() =>
  Math.min(currentPage.value * itemsPerPage, totalResults.value)
)

const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value)
    currentPage.value = page
}

const goBack = () => {
  const activeRole = localStorage.getItem('active_role')

  if (activeRole === 'Admin') {
    router.push({
      name: 'ViewResponsesAdmin',
      params: { examId }
    })
  }
  else if (activeRole === 'Faculty') {
    router.push({
      name: 'ViewResponsesFaculty',
      params: { examId }
    })
  }
  else {
    router.push('/')
  }
}

onMounted(async () => {

  // ✅ USE YOUR NEW RESULT ROUTE
  const res = await axios.get(`/exam/${examId}/results`, {
    params: {
      email: localStorage.getItem("email"),
      role: localStorage.getItem("active_role")
    }
  })

  if (res.data.success) {
    results.value = res.data.results
    examName.value = res.data.exam_name
    examDate.value = res.data.exam_date
    examTime.value = res.data.exam_time
  }
})

const downloadPDF = () => {
  if (!results.value.length) {
    alert("No results available")
    return
  }

  const doc = new jsPDF("p", "mm", "a4")

  const sortedResults = [...results.value].sort(
    (a, b) => a.Applicant_Id - b.Applicant_Id
  )

  /* ================= HEADER ================= */

  // Main Heading
  doc.setFont("helvetica", "bold")
  doc.setFontSize(18)
  doc.text(
    `${examName.value.toUpperCase()} EXAM RESULT`,
    105,
    20,
    { align: "center" }
  )

  doc.setFontSize(11)

  // Exam Date (Bold label, Normal value)
  doc.setFont("helvetica", "bold")
  doc.text("Exam Date: ", 14, 32)

  doc.setFont("helvetica", "normal")
  doc.text(`${examDate.value || "-"}`, 38, 32)

  // Exam Time (Bold label, Normal value)
  doc.setFont("helvetica", "bold")
  doc.text("Exam Time: ", 130, 32)

  doc.setFont("helvetica", "normal")
  doc.text(`${examTime.value || "-"}`, 155, 32)

  // Divider Line
  doc.line(14, 38, 196, 38)

  /* ================= TABLE ================= */

  autoTable(doc, {
    startY: 44,

    head: [
      ["Student ID", "Student Name", "Marks"]
    ],

    body: sortedResults.map(s => [
      s.Applicant_Id,
      s.Student_Name,
      s.Marks_Obtained
    ]),

    theme: "grid",

    styles: {
      font: "helvetica",
      fontSize: 11,
      textColor: [0, 0, 0],
      lineColor: [0, 0, 0],
      lineWidth: 0.2
    },

    headStyles: {
      fillColor: false,
      textColor: [0, 0, 0],
      fontStyle: "bold"
    },

    columnStyles: {
      0: { halign: "center" },
      1: { halign: "left" },
      2: { halign: "center" }
    }
  })

  /* ================= FOOTER ================= */

  doc.setFontSize(10)
  doc.text(
    `Generated on: ${new Date().toLocaleString()}`,
    105,
    285,
    { align: "center" }
  )

  doc.save(`${examName.value.replace(/\s+/g, "_")}_Exam_Result.pdf`)
}

</script>

<style scoped>

.bg-clip-text {
  -webkit-background-clip: text;
  background-clip: text;
}

</style>