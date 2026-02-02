<template>
  <div class="space-y-6">

    <!-- ---------------- CREATE EXAM BUTTON ---------------- -->
    <div class="flex gap-4 mb-6">
      <button
        @click="toggleCreateForm"
        class="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all hover:scale-105"
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


    <!-- ---------------- UPCOMING EXAMS TABLE ---------------- -->
    <div class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-200">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gradient-to-r from-blue-50 to-blue-100">
            <tr>
              <th class="py-4 px-6 font-semibold text-blue-900">ID</th>
              <th class="py-4 px-6 font-semibold text-blue-900">Exam Name</th>
              <th class="py-4 px-6 font-semibold text-blue-900">Date</th>
              <th class="py-4 px-6 font-semibold text-blue-900">Time</th>
              <th class="py-4 px-6 font-semibold text-blue-900">Duration</th>
              <th class="py-4 px-6 font-semibold text-blue-900">Questions</th>
              <th class="py-4 px-6 font-semibold text-blue-900">Max Marks</th>
              <th class="py-4 px-6 font-semibold text-blue-900">Actions</th>
            </tr>
          </thead>

          <tbody class="divide-y divide-gray-100">
            <tr
              v-for="(exam, i) in upcomingExams"
              :key="exam.Exam_Id"
              class="hover:bg-gray-50 transition"
            >
              <td class="py-4 px-6">{{ i + 1 }}</td>
              <td class="py-4 px-6">{{ exam.Exam_Name }}</td>
              <td class="py-4 px-6">{{ formatDate(exam.Exam_Date) }}</td>
              <td class="py-4 px-6">{{ exam.Exam_Time }}</td>
              <td class="py-4 px-6">{{ exam.Duration_Minutes }} min</td>
              <td class="py-4 px-6">{{ exam.Total_Questions }}</td>
              <td class="py-4 px-6">{{ exam.Max_Marks }}</td>

              <td class="py-4 px-6">
                <div class="space-y-2">
                  
                  <!-- Row 1: Add Students + Question Bank with Status -->
                  <div class="flex items-center justify-center gap-2">
                    <div class="flex items-center gap-1">
                    <button
                      @click.stop="addStudents(exam.Exam_Id)"
                      class="flex items-center gap-1 bg-blue-400 hover:bg-blue-500 text-white px-3 py-1.5 rounded-full text-xs font-semibold shadow hover:scale-105 transition-all duration-200"
                    >
                      Add Students
                    </button>

                      <!-- ✅ STATUS -->
                      <span
                        v-if="hasAssignedStudents(exam)"
                        class="text-green-600 text-lg"
                        title="Students Assigned"
                      >
                        ✔
                      </span>

                      <span
                        v-else
                        class="text-yellow-600 text-lg"
                        title="No Students Assigned"
                      >
                        ⏳
                      </span>
                    </div>
                    <button
                      @click="goAddQuestions(exam.Exam_Id)"
                      class="bg-green-500 hover:bg-green-600 text-white px-3 py-1.5 rounded-lg text-xs font-semibold shadow-sm hover:shadow transition-all"
                    >
                      Question Bank
                    </button>
                    
                    <span 
                      class="text-base flex-shrink-0" 
                      :class="examStatus?.[exam.Exam_Id]?.has_question_bank ? 'text-green-600' : 'text-yellow-500'" 
                      :title="examStatus?.[exam.Exam_Id]?.has_question_bank ? 'Completed' : 'Pending'"
                    >
                      {{ examStatus?.[exam.Exam_Id]?.has_question_bank ? '✓' : '⏳' }}
                    </span>
                  </div>

                  <!-- Row 2: Question Paper with Status + Delete -->
                  <div class="flex items-center justify-between gap-2">
                    <div class="flex items-center gap-2">
                      <button
                        @click="goMakeQuestionPaper(exam.Exam_Id)"
                        class="bg-purple-500 hover:bg-purple-600 text-white px-3 py-1.5 rounded-lg text-xs font-semibold shadow-sm hover:shadow transition-all"
                      >
                        Question Paper
                      </button>
                      
                      <span 
                        class="text-base flex-shrink-0" 
                        :class="examStatus?.[exam.Exam_Id]?.has_question_paper ? 'text-green-600' : 'text-yellow-500'" 
                        :title="examStatus?.[exam.Exam_Id]?.has_question_paper ? 'Completed' : 'Pending'"
                      >
                        {{ examStatus?.[exam.Exam_Id]?.has_question_paper ? '✓' : '⏳' }}
                      </span>
                    </div>

                    <!-- Delete Button on the right -->
                    <button
                      @click="deleteExam(exam.Exam_Id)"
                      class="bg-red-500 hover:bg-red-600 text-white px-3 py-1.5 rounded-lg text-xs font-semibold shadow-sm hover:shadow transition-all flex items-center gap-1"
                    >
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                      Delete
                    </button>
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <p v-if="upcomingExams.length === 0" class="text-center py-6 text-gray-500">
        No upcoming exams.
      </p>
    </div>

    <!-- ---------------- CONDUCTED EXAMS TABLE ---------------- -->
    <div
      v-if="conductedExams.length"
      class="mt-12 bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-200"
    >
      <div class="px-6 py-4 bg-gradient-to-r from-purple-50 to-purple-100 border-b">
        <h2 class="text-2xl font-bold text-purple-900">Conducted Exams</h2>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gradient-to-r from-blue-50 to-blue-100">
            <tr>
              <th class="py-4 px-6 font-semibold text-blue-900">ID</th>
              <th class="py-4 px-6 font-semibold text-blue-900">Exam Name</th>
              <th class="py-4 px-6 font-semibold text-blue-900">Date</th>
              <th class="py-4 px-6 font-semibold text-blue-900">Faculty Email</th>
              <th class="py-4 px-6 font-semibold text-blue-900">Students</th>
              <th class="py-4 px-6 font-semibold text-blue-900">Attempted</th>
              <th class="py-4 px-6 font-semibold text-blue-900 text-center">Actions</th>
            </tr>
          </thead>

          <tbody class="divide-y divide-gray-100">
            <tr
              v-for="(exam, i) in paginatedConductedExams"
              :key="exam.Exam_Id"
              class="hover:bg-gray-50 transition"
            >
              <td class="py-4 px-6">{{ (currentConductedPage - 1) * itemsPerPage + i + 1 }}</td>
              <td class="py-4 px-6">{{ exam.Exam_Name }}</td>
              <td class="py-4 px-6">{{ formatDate(exam.Exam_Date) }}</td>
              <td class="py-4 px-6">{{ exam.faculty_email || "N/A" }}</td>
              <td class="py-4 px-6">{{ exam.total_applicants }}</td>
              <td class="py-4 px-6">{{ exam.attempted_applicants }}</td>

              <td class="py-4 px-6 text-center">
                <button
                  @click="goViewResponses(exam.Exam_Id)"
                  class="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded-lg text-sm transition hover:scale-105"
                >
                  View Responses
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination for Conducted Exams -->
      <div class="bg-gray-50 px-6 py-4 border-t border-gray-200">
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

            <!-- First Page -->
            <button
              v-if="showConductedFirstPage"
              @click="goToConductedPage(1)"
              class="px-4 py-2 rounded-lg border transition"
              :class="currentConductedPage === 1 
                ? 'bg-blue-600 text-white border-blue-600' 
                : 'border-gray-300 bg-white hover:bg-gray-50'"
            >
              1
            </button>

            <!-- Left Ellipsis -->
            <span v-if="showConductedLeftEllipsis" class="px-2 text-gray-500">...</span>

            <!-- Page Numbers -->
            <button
              v-for="page in visibleConductedPages"
              :key="page"
              @click="goToConductedPage(page)"
              class="px-4 py-2 rounded-lg border transition"
              :class="currentConductedPage === page 
                ? 'bg-blue-600 text-white border-blue-600' 
                : 'border-gray-300 bg-white hover:bg-gray-50'"
            >
              {{ page }}
            </button>

            <!-- Right Ellipsis -->
            <span v-if="showConductedRightEllipsis" class="px-2 text-gray-500">...</span>

            <!-- Last Page -->
            <button
              v-if="showConductedLastPage"
              @click="goToConductedPage(totalConductedPages)"
              class="px-4 py-2 rounded-lg border transition"
              :class="currentConductedPage === totalConductedPages 
                ? 'bg-blue-600 text-white border-blue-600' 
                : 'border-gray-300 bg-white hover:bg-gray-50'"
            >
              {{ totalConductedPages }}
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

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const emit = defineEmits(["toast"]);

const router = useRouter();
const API = "http://localhost:5000/api";

/* ================= STATE ================= */
const examsList = ref([]);
const conductedList = ref([]);
const examStatus = ref({});

const hasAssignedStudents = (exam) => {
  return exam.total_applicants && exam.total_applicants > 0
}

const adminEmail =
  localStorage.getItem("admin_email") ||
  localStorage.getItem("email") || "";

/* ================= PAGINATION STATE ================= */
const itemsPerPage = ref(15);

// Conducted Exams Pagination
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

const visibleConductedPages = computed(() => {
  const pages = [];
  const maxVisible = 5;
  
  let start = Math.max(2, currentConductedPage.value - 2);
  let end = Math.min(totalConductedPages.value - 1, currentConductedPage.value + 2);
  
  if (currentConductedPage.value <= 3) {
    end = Math.min(maxVisible, totalConductedPages.value - 1);
    start = 2;
  }
  
  if (currentConductedPage.value >= totalConductedPages.value - 2) {
    start = Math.max(2, totalConductedPages.value - maxVisible + 1);
    end = totalConductedPages.value - 1;
  }
  
  for (let i = start; i <= end; i++) {
    pages.push(i);
  }
  
  return pages;
});

const showConductedFirstPage = computed(() => {
  return totalConductedPages.value > 1 && !visibleConductedPages.value.includes(1);
});

const showConductedLastPage = computed(() => {
  return totalConductedPages.value > 1 && !visibleConductedPages.value.includes(totalConductedPages.value);
});

const showConductedLeftEllipsis = computed(() => {
  return visibleConductedPages.value.length > 0 && visibleConductedPages.value[0] > 2;
});

const showConductedRightEllipsis = computed(() => {
  return visibleConductedPages.value.length > 0 && visibleConductedPages.value[visibleConductedPages.value.length - 1] < totalConductedPages.value - 1;
});

const goToConductedPage = (page) => {
  if (page >= 1 && page <= totalConductedPages.value) {
    currentConductedPage.value = page;
    window.scrollTo({ top: 0, behavior: 'smooth' });
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
    const res = await axios.delete(`http://localhost:5000/api/admin/exam/delete/${id}`)
    if (res.data.success) {
      emit("toast", { message: "Exam deleted successfully!", type: "success" });
      fetchExams();
      fetchConducted();
    }
  } catch {
    emit("toast", { message: "Error deleting exam", type: "error" });
  }
};

/* ================= NAVIGATION ================= */
const goAddStudents = (id) =>
  router.push({ name: "AddApplicantsExam", params: { examId: id } });

const goAddQuestions = (id) =>
  router.push({ name: "AddQuestion", params: { examId: id } });

const goMakeQuestionPaper = (id) =>
  router.push({ name: "MakeQuestionPaper", params: { examId: id } });

const goViewResponses = (id) =>
  router.push({ name: "ViewResponsesAdmin", params: { examId: id } });

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