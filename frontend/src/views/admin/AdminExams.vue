<template>
  <div class="space-y-6">

    <!-- ---------------- CREATE EXAM BUTTON ---------------- -->
    <div class="flex gap-4 mb-6">
      <button
        @click="toggleCreateForm"
        class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all hover:scale-105"
      >
        {{ showCreateForm ? "Close" : "Create Exam" }}
      </button>
    </div>

    <!-- ---------------- CREATE EXAM FORM ---------------- -->
    <div
      v-if="showCreateForm"
      class="max-w-3xl mx-auto mb-10 bg-white/80 backdrop-blur-lg shadow-xl border border-white/40 rounded-2xl p-8 transition-all"
    >
      <h2 class="text-2xl font-bold mb-6 text-gray-800">
        Create New Exam
      </h2>

      <form @submit.prevent="createExam" class="space-y-6">

        <!-- GRID -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">

          <!-- Exam Name -->
          <div class="flex flex-col gap-1">
            <label class="font-semibold text-gray-700">Exam Name</label>
            <input
              v-model="examForm.exam_name"
              type="text"
              placeholder="Enter exam name"
              required
              class="w-full border border-gray-300 px-4 py-2.5 rounded-xl focus:ring-2 focus:ring-blue-400 focus:border-blue-500 outline-none transition"
            />
          </div>

          <!-- Exam Date -->
          <div class="flex flex-col gap-1">
            <label class="font-semibold text-gray-700">Exam Date</label>
            <input
              v-model="examForm.exam_date"
              type="date"
              :min="today"
              required
              class="w-full border border-gray-300 px-4 py-2.5 rounded-xl focus:ring-2 focus:ring-blue-400 focus:border-blue-500 outline-none transition"
            />
          </div>

          <!-- Exam Time -->
          <div class="flex flex-col gap-1">
            <label class="font-semibold text-gray-700">Exam Time</label>
            <input
              v-model="examForm.exam_time"
              type="time"
              required
              class="w-full border border-gray-300 px-4 py-2.5 rounded-xl focus:ring-2 focus:ring-blue-400 focus:border-blue-500 outline-none transition"
            />
          </div>

          <!-- Duration -->
          <div class="flex flex-col gap-1">
            <label class="font-semibold text-gray-700">Duration (Minutes)</label>
            <input
              v-model="examForm.duration"
              type="number"
              min="1"
              placeholder="e.g., 60"
              required
              class="w-full border border-gray-300 px-4 py-2.5 rounded-xl focus:ring-2 focus:ring-blue-400 focus:border-blue-500 outline-none transition"
            />
          </div>

          <!-- Total Questions -->
          <div class="flex flex-col gap-1">
            <label class="font-semibold text-gray-700">Total Questions</label>
            <input
              v-model="examForm.total_questions"
              type="number"
              min="1"
              placeholder="e.g., 50"
              required
              class="w-full border border-gray-300 px-4 py-2.5 rounded-xl focus:ring-2 focus:ring-blue-400 focus:border-blue-500 outline-none transition"
            />
          </div>

          <!-- Max Marks -->
          <div class="flex flex-col gap-1">
            <label class="font-semibold text-gray-700">Maximum Marks</label>
            <input
              v-model="examForm.max_marks"
              type="number"
              min="1"
              placeholder="e.g., 100"
              required
              class="w-full border border-gray-300 px-4 py-2.5 rounded-xl focus:ring-2 focus:ring-blue-400 focus:border-blue-500 outline-none transition"
            />
          </div>

        </div>

        <!-- Footer Buttons -->
        <div class="flex justify-end gap-4 pt-4">
          <button
            type="button"
            @click="clearExamForm"
            class="bg-gray-300 text-gray-700 px-6 py-2 rounded-xl hover:bg-gray-400 transition font-semibold shadow-md hover:shadow-lg"
          >
            Clear
          </button>
          <button
            type="submit"
            class="bg-blue-600 text-white px-6 py-2 rounded-xl hover:bg-blue-700 transition font-semibold shadow-md hover:shadow-lg"
          >
            Create Exam
          </button>
        </div>

      </form>
    </div>

    <!-- ---------------- CREATED EXAMS TABLE ---------------- -->
    <div v-if="upcomingExams.length" class="mt-8">
      <h2 class="text-2xl font-semibold mb-4 text-gray-800">Created Exams</h2>
      <div class="bg-white rounded-xl shadow-lg overflow-hidden">
        <table class="min-w-full">
          <thead class="bg-gradient-to-r from-blue-50 to-indigo-50">
            <tr>
              <th class="px-3 py-4 text-left text-sm font-bold text-gray-700 whitespace-nowrap">Exam Name</th>
              <th class="px-3 py-4 text-left text-sm font-bold text-gray-700 whitespace-nowrap">Date</th>
              <th class="px-3 py-4 text-left text-sm font-bold text-gray-700 whitespace-nowrap">Time</th>
              <th class="px-3 py-4 text-left text-sm font-bold text-gray-700 whitespace-nowrap">Duration</th>
              <th class="px-2 py-4 text-left text-sm font-bold text-gray-700">Questions</th>
              <th class="px-2 py-4 text-left text-sm font-bold text-gray-700">Max Marks</th>
              <th class="px-2 py-4 text-center text-sm font-bold text-gray-700">QR Code</th>
              <th class="px-6 py-4 text-center text-sm font-bold text-gray-700 min-w-[420px]">Actions</th>
              <th class="px-2 py-4 text-center text-sm font-bold text-gray-700">Delete</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="exam in upcomingExams" :key="exam.Exam_Id" class="hover:bg-gray-50 transition">
              <td class="px-3 py-4 text-sm text-gray-800 font-medium">{{ exam.Exam_Name }}</td>
              <td class="px-3 py-4 text-sm text-gray-600 whitespace-nowrap">{{ exam.Exam_Date }}</td>
              <td class="px-3 py-4 text-sm text-gray-600 whitespace-nowrap">{{ exam.Exam_Time }}</td>
              <td class="px-3 py-4 text-sm text-gray-600 whitespace-nowrap">{{ exam.Duration_Minutes }} min</td>
              <td class="px-2 py-4 text-sm text-gray-600 text-center">{{ exam.Total_Questions }}</td>
              <td class="px-2 py-4 text-sm text-gray-600 text-center">{{ exam.Max_Marks }}</td>
              
              <!-- QR Code Column -->
              <td class="px-2 py-4 text-center">
                <button
                  @click="openQRModal(exam.Exam_Id, exam.Exam_Name)"
                  class="inline-flex items-center justify-center w-10 h-10 bg-indigo-500 hover:bg-indigo-600 rounded-lg transition-all duration-200 shadow-md hover:shadow-lg hover:scale-110"
                  title="Generate QR Code"
                >
                  <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z" />
                  </svg>
                </button>
              </td>
              
              <!-- Actions Column -->
              <td class="px-6 py-4">  
                <div class="flex items-center justify-center gap-2.5">
                  
                  <!-- Add Students -->
                  <div class="relative">
                    <button
                      @click.stop="addStudents(exam.Exam_Id)"
                      class="bg-blue-400 hover:bg-blue-500 text-white px-3.5 py-2 rounded-lg text-xs font-semibold shadow-md hover:shadow-lg transition-all duration-200 hover:scale-105 whitespace-nowrap"
                    >
                      Add Students
                    </button>
                    <!-- Status Indicator -->
                    <span
                      v-if="hasAssignedStudents(exam)"
                      class="absolute -top-0.5 -right-0.5 text-green-600 text-sm bg-white rounded-full w-4 h-4 flex items-center justify-center"
                      title="Students Assigned"
                    >
                      ✔
                    </span>
                    <span
                      v-else
                      class="absolute -top-0.5 -right-0.5 text-yellow-600 text-sm bg-white rounded-full w-4 h-4 flex items-center justify-center"
                      title="No Students Assigned"
                    >
                      ⏳
                    </span>
                  </div>

                  <!-- Question Bank -->
                  <div class="relative">
                    <button
                      @click="navigateTo('AddQuestion', exam.Exam_Id)"
                      class="bg-green-500 hover:bg-green-600 text-white px-3.5 py-2 rounded-lg text-xs font-semibold shadow-md hover:shadow-lg transition-all duration-200 hover:scale-105 whitespace-nowrap"
                    >
                      Question Bank
                    </button>
                    <!-- Status Indicator -->
                    <span
                      v-if="examStatus[exam.Exam_Id]?.has_question_bank"
                      class="absolute -top-0.5 -right-0.5 text-green-600 text-sm bg-white rounded-full w-4 h-4 flex items-center justify-center"
                      title="Completed"
                    >
                      ✔
                    </span>
                    <span
                      v-else
                      class="absolute -top-0.5 -right-0.5 text-yellow-600 text-sm bg-white rounded-full w-4 h-4 flex items-center justify-center"
                      title="Pending"
                    >
                      ⏳
                    </span>
                  </div>

                  <!-- Question Paper -->
                  <div class="relative">
                    <button
                      @click="navigateTo('MakeQuestionPaper', exam.Exam_Id)"
                      class="bg-purple-500 hover:bg-purple-600 text-white px-3.5 py-2 rounded-lg text-xs font-semibold shadow-md hover:shadow-lg transition-all duration-200 hover:scale-105 whitespace-nowrap"
                    >
                      Question Paper
                    </button>
                    <!-- Status Indicator -->
                    <span
                      v-if="examStatus[exam.Exam_Id]?.has_question_paper"
                      class="absolute -top-0.5 -right-0.5 text-green-600 text-sm bg-white rounded-full w-4 h-4 flex items-center justify-center"
                      title="Completed"
                    >
                      ✔
                    </span>
                    <span
                      v-else
                      class="absolute -top-0.5 -right-0.5 text-yellow-600 text-sm bg-white rounded-full w-4 h-4 flex items-center justify-center"
                      title="Pending"
                    >
                      ⏳
                    </span>
                  </div>

                </div>
              </td>

              <!-- Delete Column -->
              <td class="px-2 py-4 text-center">
                <button
                  @click="deleteExam(exam.Exam_Id)"
                  class="inline-flex items-center justify-center w-10 h-10 bg-red-500 hover:bg-red-600 rounded-lg transition-all duration-200 shadow-md hover:shadow-lg hover:scale-110"
                  title="Delete Exam"
                >
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-else class="mt-8 text-gray-500 text-center text-lg py-12 bg-white rounded-xl shadow">
      No exams created yet.
    </div>

    <!-- ---------------- CONDUCTED EXAMS TABLE ---------------- -->
    <div v-if="conductedExams && conductedExams.length" class="mt-12">
      <h2 class="text-2xl font-semibold mb-4 text-gray-800">Conducted Exams</h2>
      <div class="bg-white rounded-xl shadow-lg overflow-hidden">
        <table class="min-w-full">
          <thead class="bg-gradient-to-r from-blue-50 to-indigo-50">
            <tr>
              <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Exam Name</th>
              <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Date</th>
              <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Total Applicants</th>
              <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Attempted</th>
              <th class="px-6 py-4 text-center text-sm font-bold text-gray-700">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="exam in paginatedConductedExams" :key="exam.Exam_Id" class="hover:bg-gray-50 transition">
              <td class="px-6 py-4 text-sm text-gray-800 font-medium">{{ exam.Exam_Name || 'N/A' }}</td>
              <td class="px-6 py-4 text-sm text-gray-600">{{ formatDate(exam.Exam_Date) }}</td>
              <td class="px-6 py-4 text-sm text-gray-600">{{ exam.total_applicants || 0 }}</td>
              <td class="px-6 py-4 text-sm text-gray-600">{{ exam.attempted_applicants || 0 }}</td>
              <td class="px-6 py-4 text-center">
                <button
                  @click="navigateTo('ViewResponsesAdmin', exam.Exam_Id)"
                  class="bg-purple-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-purple-700 shadow-md hover:shadow-lg transition font-semibold"
                >
                  View Responses
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination for Conducted Exams -->
      <div v-if="conductedExams.length > 0" class="bg-gray-50 px-6 py-4 border-t border-gray-200">
        <div class="flex items-center justify-between">
          
          <!-- Results Info -->
          <div class="text-sm text-gray-700">
            Showing 
            <span class="font-semibold">{{ conductedStartIndex + 1 }}</span>
            to 
            <span class="font-semibold">{{ conductedEndIndex }}</span>
            of 
            <span class="font-semibold">{{ totalConductedExams }}</span>
            results
          </div>

          <!-- Pagination Buttons -->
          <div class="flex items-center gap-2">
            
            <!-- Previous Button -->
            <button
              @click="goToConductedPage(currentConductedPage - 1)"
              :disabled="currentConductedPage === 1"
              class="px-3 py-2 rounded-lg border border-gray-300 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
              </svg>
            </button>

            <!-- Page Numbers -->
            <button
              v-for="page in totalConductedPages"
              :key="page"
              @click="goToConductedPage(page)"
              class="px-4 py-2 rounded-lg border transition"
              :class="currentConductedPage === page 
                ? 'bg-blue-600 text-white border-blue-600' 
                : 'border-gray-300 bg-white hover:bg-gray-50'"
            >
              {{ page }}
            </button>

            <!-- Next Button -->
            <button
              @click="goToConductedPage(currentConductedPage + 1)"
              :disabled="currentConductedPage === totalConductedPages"
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

    <!-- QR Code Modal -->
    <QRCodeModal
      :is-open="showQRModal"
      :exam-id="selectedExamForQR?.id || ''"
      :exam-name="selectedExamForQR?.name || ''"
      @close="closeQRModal"
    />


  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import QRCodeModal from "@/components/QRCodeModal.vue";

const emit = defineEmits(["toast"]);
const router = useRouter();
const API = "http://localhost:5000/api";

/* ================= STATE ================= */
const examsList = ref([]);
const conductedList = ref([]);
const examStatus = ref({});

// QR Code Modal State
const showQRModal = ref(false);
const selectedExamForQR = ref(null);

const adminEmail = localStorage.getItem("admin_email") || localStorage.getItem("email") || "";

/* ================= PAGINATION STATE ================= */
const itemsPerPage = ref(15);
const currentConductedPage = ref(1);

/* ================= FORM STATE ================= */
const showCreateForm = ref(false);

const examForm = ref({
  exam_name: "",
  exam_date: "",
  exam_time: "",
  duration: "",
  total_questions: "",
  max_marks: "",
  faculty_email: adminEmail,
});

const clearExamForm = () => {
  examForm.value = {
    exam_name: "",
    exam_date: "",
    exam_time: "",
    duration: "",
    total_questions: "",
    max_marks: "",
    faculty_email: adminEmail
  };
};

const toggleCreateForm = () => {
  showCreateForm.value = !showCreateForm.value;
};

/* ================= QR CODE MODAL FUNCTIONS ================= */
const openQRModal = (examId, examName) => {
  selectedExamForQR.value = {
    id: examId,
    name: examName
  };
  showQRModal.value = true;
};

const closeQRModal = () => {
  showQRModal.value = false;
  selectedExamForQR.value = null;
};

/* ================= EXAM FILTERING ================= */
const isExamEnded = (exam) => {
  const [year, month, day] = exam.Exam_Date.split("-").map(Number);
  const [hours, minutes] = exam.Exam_Time.split(":").map(Number);

  const start = new Date(year, month - 1, day, hours, minutes);
  const end = new Date(start.getTime() + Number(exam.Duration_Minutes) * 60000);

  return end < new Date();
};

const upcomingExams = computed(() =>
  examsList.value.filter((exam) => !isExamEnded(exam))
);

const conductedExams = computed(() => conductedList.value);

const hasAssignedStudents = (exam) => {
  return exam.total_applicants && exam.total_applicants > 0;
};

/* ================= CONDUCTED EXAMS PAGINATION ================= */
const totalConductedExams = computed(() => conductedExams.value.length);
const totalConductedPages = computed(() => Math.ceil(totalConductedExams.value / itemsPerPage.value));

const paginatedConductedExams = computed(() => {
  const start = (currentConductedPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return conductedExams.value.slice(start, end);
});

const conductedStartIndex = computed(() => (currentConductedPage.value - 1) * itemsPerPage.value);
const conductedEndIndex = computed(() => {
  const end = currentConductedPage.value * itemsPerPage.value;
  return end > totalConductedExams.value ? totalConductedExams.value : end;
});

const goToConductedPage = (page) => {
  if (page >= 1 && page <= totalConductedPages.value) {
    currentConductedPage.value = page;
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
};

/* ================= EXAM STATUS ================= */
const loadExamStatuses = async (exams) => {
  const statusMap = {};

  for (const exam of exams) {
    try {
      const res = await axios.get(`${API}/exam/status/${exam.Exam_Id}`);

      if (res.data.success) {
        statusMap[exam.Exam_Id] = res.data.status;
      } else {
        statusMap[exam.Exam_Id] = {
          has_question_bank: false,
          has_question_paper: false
        };
      }
    } catch {
      statusMap[exam.Exam_Id] = {
        has_question_bank: false,
        has_question_paper: false
      };
    }
  }

  examStatus.value = statusMap;
};

/* ================= FETCH EXAMS ================= */
const fetchExams = async () => {
  try {
    const res = await axios.get(`${API}/exam/get_exams/${adminEmail}`);
    if (res.data.success) {
      examsList.value = res.data.exams;
      await loadExamStatuses(res.data.exams);
    } else {
      examsList.value = [];
    }
  } catch {
    examsList.value = [];
  }
};

/* ================= FETCH CONDUCTED ================= */
const fetchConducted = async () => {
  try {
    const res = await axios.get(`${API}/admin/conducted_exams`);
    if (res.data.success) {
      conductedList.value = res.data.exams;
    }
  } catch {
    emit("toast", { message: "Error fetching conducted exams", type: "error" });
  }
};

/* ================= CREATE EXAM ================= */
const createExam = async () => {
  try {
    const res = await axios.post(`${API}/exam/create`, examForm.value);

    if (res.data.success) {
      emit("toast", { message: "Exam created successfully!", type: "success" });
      toggleCreateForm();
      fetchExams();

      examForm.value = {
        exam_name: "",
        exam_date: "",
        exam_time: "",
        duration: "",
        total_questions: "",
        max_marks: "",
        faculty_email: adminEmail,
      };
    }
  } catch {
    emit("toast", { message: "Error creating exam", type: "error" });
  }
};

/* ================= DELETE ================= */
const deleteExam = async (id) => {
  if (!confirm("Delete this exam?")) return;

  try {
    const res = await axios.delete(`http://localhost:5000/api/admin/exam/delete/${id}`);
    if (res.data.success) {
      emit("toast", { message: "Exam deleted successfully!", type: "success" });
      fetchExams();
      fetchConducted();
    }
  } catch {
    emit("toast", { message: "Error deleting exam", type: "error" });
  }
};

/* ================= ADD STUDENTS ================= */
const addStudents = (examId) => {
  if (!examId) {
    alert("Invalid exam ID");
    return;
  }

  router.push({
    name: 'AddApplicantsExam',
    params: { examId }
  });
};

/* ================= NAVIGATION HELPER ================= */
const navigateTo = (routeName, examId) => {
  if (!examId) {
    alert("Invalid exam ID");
    return;
  }

  router.push({
    name: routeName,
    params: { examId }
  });
};

const today = new Date().toISOString().slice(0, 10);
const formatDate = (d) => new Date(d).toLocaleDateString("en-IN");

/* ================= MOUNTED ================= */
onMounted(() => {
  fetchExams();
  fetchConducted();

  setInterval(() => {
    fetchExams();
    fetchConducted();
  }, 60000);
});
</script>

<style scoped>
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