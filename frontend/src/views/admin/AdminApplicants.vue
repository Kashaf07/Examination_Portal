<template>
  <div class="space-y-6">

    <!-- TOP ACTION BAR -->
    <div class="flex items-start gap-6 mb-6">

      <!-- LEFT: Add / Upload Buttons -->
      <div class="flex gap-4">
        <button
          @click="toggleAddApplicant"
          class="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all hover:scale-105"
        >
          {{ showAddApplicantPage ? 'Close' : 'Add Students' }}
        </button>

        <button
          @click="navigateUpload"
          class="bg-purple-500 hover:bg-purple-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all hover:scale-105"
        >
          {{ showUploadPage ? 'Close' : 'Upload Students' }}
        </button>
      </div>

      <!-- RIGHT: Active / All Toggle -->
      <div class="flex flex-col">
        <div class="flex items-center bg-gray-100 rounded-full p-1 shadow-inner w-fit">
          <button
            @click="showDisabled = false"
            :class="[
              'px-4 py-2 text-sm font-semibold rounded-full transition-all',
              !showDisabled
                ? 'bg-white text-blue-600 shadow'
                : 'text-gray-600 hover:text-gray-800'
            ]"
          >
            Active Only
          </button>

          <button
            @click="showDisabled = true"
            :class="[
              'px-4 py-2 text-sm font-semibold rounded-full transition-all',
              showDisabled
                ? 'bg-white text-blue-600 shadow'
                : 'text-gray-600 hover:text-gray-800'
            ]"
          >
            All Students
          </button>
        </div>

        <!-- Helper text JUST below toggle -->
        <p
          v-if="showDisabled"
          class="text-xs text-gray-500 mt-1 pl-2"
        >
          Disabled students are shown in grey
        </p>
      </div>

    </div>

    <div v-if="showAddApplicantPage" class="mb-8"></div>

    <!-- Add Applicant Page -->
    <AddApplicantsPage
      v-if="showAddApplicantPage"
      @close="showAddApplicantPage = false"
      @saved="handleApplicantSaved"
    />

    <!-- Upload Students Page -->    
    <UploadStudents
      v-if="showUploadPage"
      @close="showUploadPage = false"
    />

    <div v-if="!showAddApplicantPage && !showUploadPage" class="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden">
      <!-- Applicants Table -->
      <div class="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden">

        <table class="w-full">
          <thead class="bg-gradient-to-r from-blue-50 to-blue-100 text-gray-700">
            <tr>
              <th class="py-4 px-6">
                <input
                  type="checkbox"
                  @change="toggleAll"
                  :checked="selectedApplicants.length === paginatedApplicants.length && paginatedApplicants.length > 0"
                />
              </th>
              <th class="py-4 px-6 font-semibold">ID</th>
              <th class="py-4 px-6 font-semibold">Name</th>
              <th class="py-4 px-6 font-semibold">Email</th>
              <th class="py-4 px-6 font-semibold">Phone</th>
              <th class="py-4 px-6 font-semibold">Actions</th>
            </tr>
          </thead>

          <tbody class="divide-y divide-gray-100">
            <tr
              v-for="(a, i) in paginatedApplicants"
              :key="a.Applicant_Id"
              :class="['transition',Number(a.Is_Active) === 0? 'opacity-50 bg-gray-100 cursor-not-allowed': 'hover:bg-blue-50']"
            >
              <td class="px-6 py-5">
                <input type="checkbox" :value="a.Applicant_Id" v-model="selectedApplicants" />
              </td>

              <td class="px-6 py-5">{{ startIndex + i + 1 }}</td>
              <td class="px-6 py-5 font-medium text-gray-800">{{ a.Full_Name }}</td>
              <td class="px-6 py-5">{{ a.Email }}</td>
              <td class="px-6 py-5">{{ a.Phone }}</td>

              <td class="px-6 py-5 flex gap-2">
                <button
                  @click="openViewModal(a)"
                  class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md shadow"
                >
                  View
                </button>

                <button
                  @click="toggleApplicantStatus(a)"
                  :class="a.Is_Active === 1
                    ? 'bg-red-500 hover:bg-red-600'
                    : 'bg-green-500 hover:bg-green-600'"
                  class="text-white px-4 py-2 rounded-md shadow transition hover:scale-105"
                >
                  {{ a.Is_Active === 1 ? 'Disable' : 'Enable' }}
                </button>
              </td>
            </tr>
          </tbody>

        </table>

        <div v-if="!applicantsList.length" class="text-center py-10 text-gray-500">
          No Students found
        </div>

        <!-- Pagination Controls -->
        <div v-if="applicantsList.length > 0" class="bg-gray-50 px-6 py-4 border-t border-gray-200">
          <div class="flex items-center justify-between">
            
            <!-- Results Info -->
            <div class="text-sm text-gray-700">
              Showing 
              <span class="font-semibold">{{ startIndex + 1 }}</span>
              to 
              <span class="font-semibold">{{ endIndex }}</span>
              of 
              <span class="font-semibold">{{ totalApplicants }}</span>
              results
            </div>

            <!-- Pagination Buttons -->
            <div class="flex items-center gap-2">
              
              <!-- Previous Button -->
              <button
                @click="goToPage(currentPage - 1)"
                :disabled="currentPage === 1"
                class="px-3 py-2 rounded-lg border border-gray-300 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
                :class="{ 'cursor-not-allowed': currentPage === 1 }"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
                </svg>
              </button>

              <!-- First Page -->
              <button
                v-if="showFirstPage"
                @click="goToPage(1)"
                class="px-4 py-2 rounded-lg border transition"
                :class="currentPage === 1 
                  ? 'bg-blue-600 text-white border-blue-600' 
                  : 'border-gray-300 bg-white hover:bg-gray-50'"
              >
                1
              </button>

              <!-- Left Ellipsis -->
              <span v-if="showLeftEllipsis" class="px-2 text-gray-500">...</span>

              <!-- Page Numbers -->
              <button
                v-for="page in visiblePages"
                :key="page"
                @click="goToPage(page)"
                class="px-4 py-2 rounded-lg border transition"
                :class="currentPage === page 
                  ? 'bg-blue-600 text-white border-blue-600' 
                  : 'border-gray-300 bg-white hover:bg-gray-50'"
              >
                {{ page }}
              </button>

              <!-- Right Ellipsis -->
              <span v-if="showRightEllipsis" class="px-2 text-gray-500">...</span>

              <!-- Last Page -->
              <button
                v-if="showLastPage"
                @click="goToPage(totalPages)"
                class="px-4 py-2 rounded-lg border transition"
                :class="currentPage === totalPages 
                  ? 'bg-blue-600 text-white border-blue-600' 
                  : 'border-gray-300 bg-white hover:bg-gray-50'"
              >
                {{ totalPages }}
              </button>

              <!-- Next Button -->
              <button
                @click="goToPage(currentPage + 1)"
                :disabled="currentPage === totalPages"
                class="px-3 py-2 rounded-lg border border-gray-300 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
                :class="{ 'cursor-not-allowed': currentPage === totalPages }"
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

        
    <!-- View Modal -->
    <div
      v-if="showViewModal"
      class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 px-4"
    >
      <div
        class="bg-white/90 backdrop-blur-lg rounded-2xl shadow-2xl w-full max-w-lg p-8 relative animate-fadeIn"
      >
        <!-- Close Button -->
        <button
          @click="showViewModal = false"
          class="absolute top-4 right-4 w-8 h-8 flex items-center justify-center 
                rounded-full bg-gray-200 hover:bg-gray-300 transition"
        >
          ✕
        </button>

        <h3
          class="text-2xl font-extrabold text-blue-700 mb-6 text-center tracking-wide"
        >
          Applicant Details
        </h3>

        <div class="space-y-4 text-gray-700 text-base">
          <p><span class="font-semibold text-gray-900">Name:</span> {{ selectedApplicant.Full_Name }}</p>
          <p><span class="font-semibold text-gray-900">Email:</span> {{ selectedApplicant.Email }}</p>
          <p><span class="font-semibold text-gray-900">Phone:</span> {{ selectedApplicant.Phone }}</p>
          <p><span class="font-semibold text-gray-900">DOB:</span> {{ formatDOB(selectedApplicant.DOB) }}</p>
          <p><span class="font-semibold text-gray-900">Gender:</span> {{ selectedApplicant.Gender }}</p>
          <p><span class="font-semibold text-gray-900">Reg. Date:</span> {{ formatDate(selectedApplicant.Registration_Date) }}</p>
          <p><span class="font-semibold text-gray-900">Address:</span> {{ selectedApplicant.Address }}</p>
        </div>

        <!-- Bottom Close Button -->
        <div class="mt-8 text-center">
          <button
            @click="showViewModal = false"
            class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-3 rounded-full shadow-md transition"
          >
            Close
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "@/utils/axiosInstance";
import AddApplicantsPage from "../AddApplicantsPage.vue";
import UploadStudents from "../UploadStudents.vue";

const emit = defineEmits(["toast"]);
const router = useRouter();

const applicantsList = ref([]);
const selectedApplicants = ref([]);
const showViewModal = ref(false);
const selectedApplicant = ref(null);
const showAddApplicantPage = ref(false);
const showUploadPage = ref(false);
const showDisabled = ref(false);

const filteredApplicants = computed(() => {
  if (showDisabled.value) {
    return applicantsList.value;
  }
  return applicantsList.value.filter(
    a => Number(a.Is_Active) === 1
  );
});

// ================= PAGINATION STATE =================
const currentPage = ref(1);
const itemsPerPage = ref(20);

// ================= PAGINATION COMPUTED =================
const totalApplicants = computed(() => filteredApplicants.value.length);

const totalPages = computed(() => Math.ceil(totalApplicants.value / itemsPerPage.value));

const paginatedApplicants = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return filteredApplicants.value.slice(start, end);
});

const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage.value);

const endIndex = computed(() => {
  const end = currentPage.value * itemsPerPage.value;
  return end > totalApplicants.value ? totalApplicants.value : end;
});

// Google-style pagination
const visiblePages = computed(() => {
  const pages = [];
  const maxVisible = 5;
  
  let start = Math.max(2, currentPage.value - 2);
  let end = Math.min(totalPages.value - 1, currentPage.value + 2);
  
  if (currentPage.value <= 3) {
    end = Math.min(maxVisible, totalPages.value - 1);
    start = 2;
  }
  
  if (currentPage.value >= totalPages.value - 2) {
    start = Math.max(2, totalPages.value - maxVisible + 1);
    end = totalPages.value - 1;
  }
  
  for (let i = start; i <= end; i++) {
    pages.push(i);
  }
  
  return pages;
});

const showFirstPage = computed(() => {
  return totalPages.value > 1 && !visiblePages.value.includes(1);
});

const showLastPage = computed(() => {
  return totalPages.value > 1 && !visiblePages.value.includes(totalPages.value);
});

const showLeftEllipsis = computed(() => {
  return visiblePages.value.length > 0 && visiblePages.value[0] > 2;
});

const showRightEllipsis = computed(() => {
  return visiblePages.value.length > 0 && visiblePages.value[visiblePages.value.length - 1] < totalPages.value - 1;
});

// ================= PAGINATION METHODS =================
const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
};

// ✅ FETCH
const fetchApplicants = async () => {
  const res = await axios.get("/admin/applicants");
  applicantsList.value = res.data.applicants || res.data;
  currentPage.value = 1; // Reset to first page when data refreshes
};

const handleApplicantSaved = () => {
  fetchApplicants();
  emit("toast", { message: "Applicant added", type: "success" });
};

const toggleAddApplicant = () => {
  showAddApplicantPage.value = !showAddApplicantPage.value;
  showUploadPage.value = false;

  if (!showAddApplicantPage.value) {
    fetchApplicants();
  }
};

const navigateUpload = () => {
  showUploadPage.value = !showUploadPage.value;
  showAddApplicantPage.value = false;

  if (!showUploadPage.value) {
    fetchApplicants();
  }
};

// View
const openViewModal = (a) => {
  selectedApplicant.value = a;
  showViewModal.value = true;
};

// Enable/Disable
const toggleApplicantStatus = async (applicant) => {
  const action = applicant.Is_Active === 1 ? "disable" : "enable";
  if (!confirm(`Are you sure you want to ${action} this student?`)) return;

  await axios.put(`/admin/applicants/toggle-status/${applicant.Applicant_Id}`);
  emit("toast", {
    message: `Student ${action}d successfully`,
    type: "success"
  });
  fetchApplicants();
};


const formatDOB = (dob) => {
  if (!dob) return "N/A";
  const d = new Date(dob);
  return d.toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric"
  });
};

const toggleAll = () => {
  selectedApplicants.value =
    selectedApplicants.value.length === paginatedApplicants.value.length
      ? []
      : paginatedApplicants.value.map(a => a.Applicant_Id);
};

const formatDate = (d) =>
  d ? new Date(d).toLocaleDateString("en-IN") : "N/A";

onMounted(fetchApplicants);
</script>

<style scoped>
@keyframes fadeIn {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.animate-fadeIn {
  animation: fadeIn 0.25s ease-out;
}

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