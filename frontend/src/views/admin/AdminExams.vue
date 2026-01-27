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

              <td class="py-4 px-6 space-x-2">
                <button
                  @click="goAddStudents(exam.Exam_Id)"
                  class="px-3 py-1.5 rounded-lg bg-blue-500 text-white hover:bg-blue-600 text-xs"
                >
                  Add Students
                </button>

                <button
                  @click="goAddQuestions(exam.Exam_Id)"
                  class="px-3 py-1.5 rounded-lg bg-green-500 text-white hover:bg-green-600 text-xs"
                >
                  Add Question Bank
                </button>

                <button
                  @click="goMakeQuestionPaper(exam.Exam_Id)"
                  class="px-3 py-1.5 rounded-lg bg-purple-500 text-white hover:bg-purple-600 text-xs"
                >
                  Make Question Paper
                </button>

                <button
                  @click="deleteExam(exam.Exam_Id)"
                  class="px-3 py-1.5 rounded-lg bg-red-500 text-white hover:bg-red-600 text-xs"
                >
                  Delete
                </button>
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
              v-for="(exam, i) in conductedExams"
              :key="exam.Exam_Id"
              class="hover:bg-gray-50 transition"
            >
              <td class="py-4 px-6">{{ i + 1 }}</td>
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
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const emit = defineEmits(["toast"]);

const InputField = {
  props: ["label", "type", "modelValue", "placeholder", "required", "min"],
  emits: ["update:modelValue"],
  template: `
    <div>
      <label class="block text-sm font-semibold text-gray-700 mb-2">{{ label }}</label>
      <input
        :type="type || 'text'"
        :value="modelValue"
        :required="required"
        :min="min"
        @input="$emit('update:modelValue', $event.target.value)"
        class="w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-blue-500"
        :placeholder="placeholder"
      />
    </div>
  `,
};

const router = useRouter();
const API = "http://localhost:5000/api";

const examsList = ref([]);
const conductedList = ref([]);

const adminEmail =
  localStorage.getItem("admin_email") ||
  localStorage.getItem("email") || "";

// Form state
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

// Toggle create form
const toggleCreateForm = () => {
  showCreateForm.value = !showCreateForm.value;
};

// Fetch Exams
const fetchExams = async () => {
  try {
    const res = await axios.get(`${API}/exam/get_exams/${adminEmail}`);
    if (res.data.success) {
      examsList.value = res.data.exams;
    } else {
      examsList.value = [];
    }
  } catch {
    examsList.value = [];
  }
};

// Fetch conducted exams
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

// Create Exam
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

// Helpers
const isExamEnded = (exam) => {
  // Split date
  const [year, month, day] = exam.Exam_Date.split("-").map(Number);

  // Split time safely (handles HH:mm or HH:mm:ss)
  const [hours, minutes] = exam.Exam_Time.split(":").map(Number);

  // Create LOCAL datetime (not UTC)
  const start = new Date(year, month - 1, day, hours, minutes);

  const end = new Date(
    start.getTime() + Number(exam.Duration_Minutes) * 60000
  );

  return end < new Date();
};


const upcomingExams = computed(() =>
  examsList.value.filter((exam) => !isExamEnded(exam))
);

const conductedExams = computed(() => conductedList.value);

// Delete Exam
const deleteExam = async (id) => {
  if (!confirm("Delete this exam?")) return;

  try {
    const res = await axios.delete(`${API}/exam/delete/${id}`);

    if (res.data.success) {
      emit("toast", { message: "Exam deleted successfully!", type: "success" });
      fetchExams();
      fetchConducted();
    }
  } catch {
    emit("toast", { message: "Error deleting exam", type: "error" });
  }
};

// Navigation buttons
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

// Mounted
onMounted(() => {
  fetchExams();
  fetchConducted();

  // Auto-refresh every 1 minute
  setInterval(() => {
    fetchExams();
    fetchConducted();
  }, 60000);
});
</script>
