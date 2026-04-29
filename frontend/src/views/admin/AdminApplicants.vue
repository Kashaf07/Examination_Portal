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

      <!-- RIGHT: Active / All / Inactive Toggle -->
      <div class="flex flex-col">
        <div class="flex items-center bg-gray-100 rounded-full p-1 shadow-inner w-fit">
          <button
            @click="filterMode = 'active'"
            :class="[
              'px-4 py-2 text-sm font-semibold rounded-full transition-all',
              filterMode === 'active'
                ? 'bg-white text-blue-600 shadow'
                : 'text-gray-600 hover:text-gray-800'
            ]"
          >
            Active Only
          </button>

          <button
            @click="filterMode = 'all'"
            :class="[
              'px-4 py-2 text-sm font-semibold rounded-full transition-all',
              filterMode === 'all'
                ? 'bg-white text-blue-600 shadow'
                : 'text-gray-600 hover:text-gray-800'
            ]"
          >
            All Students
          </button>

          <button
            @click="filterMode = 'inactive'"
            :class="[
              'px-4 py-2 text-sm font-semibold rounded-full transition-all',
              filterMode === 'inactive'
                ? 'bg-white text-blue-600 shadow'
                : 'text-gray-600 hover:text-gray-800'
            ]"
          >
            Inactive Only
          </button>
        </div>

        <!-- Helper text JUST below toggle -->
        <p
          v-if="filterMode === 'all'"
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

        <!-- SEARCH FILTER INPUT -->
        <div class="mb-6 flex gap-3 p-6 pb-0">
          <input
            v-model="searchQuery"
            placeholder="🔍 Search students..."
            class="w-full max-w-xs px-4 py-3 rounded-xl border-2 border-black bg-purple-50
                   focus:bg-white focus:ring-2 focus:ring-blue-400 outline-none transition 
                   text-sm font-medium placeholder:text-gray-600"
          />
        </div>

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

              <td class="px-6 py-5">
                <div class="flex items-center justify-center gap-3">
                  <button
                    @click="openEditModal(a)"
                    class="text-gray-800 hover:text-purple-600 transition-colors duration-200"
                    title="Edit Student"
                  >
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>

                  <button
                    @click="openViewModal(a)"
                    class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm shadow transition hover:scale-105"
                  >
                    View
                  </button>

                  <button
                    @click="toggleApplicantStatus(a)"
                    :class="a.Is_Active === 1
                      ? 'bg-red-500 hover:bg-red-600'
                      : 'bg-green-500 hover:bg-green-600'"
                    class="text-white px-4 py-2 rounded-lg text-sm shadow transition hover:scale-105"
                  >
                    {{ a.Is_Active === 1 ? 'Disable' : 'Enable' }}
                  </button>
                </div>
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

    <!-- Edit Modal -->
    <div
      v-if="showEditModal"
      class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 px-4"
    >
      <div
        class="bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 rounded-3xl shadow-2xl w-full max-w-2xl p-8 relative animate-fadeIn max-h-[90vh] overflow-y-auto border-2 border-purple-200"
      >
        <!-- Close Button -->
        <button
          @click="closeEditModal"
          class="absolute top-4 right-4 w-10 h-10 flex items-center justify-center 
                rounded-full bg-white/80 hover:bg-white shadow-lg hover:shadow-xl transition-all hover:rotate-90 duration-300"
        >
          <span class="text-gray-600 text-xl font-bold">✕</span>
        </button>

        <!-- Header with Icon -->
        <div class="text-center mb-8">
          <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full mb-4 shadow-lg">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </div>
          <h3 class="text-3xl font-semibold text-gray-800 tracking-tight">
            Edit Student Details
          </h3>
          <p class="text-sm text-gray-600 mt-2">Update student information below</p>
        </div>

        <form @submit.prevent="updateApplicant" class="space-y-5">
          <!-- Full Name -->
          <div class="relative">
            <label class="block text-sm font-bold text-gray-800 mb-2">
              <span class="flex items-center gap-2">
                <svg class="w-4 h-4 text-purple-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                </svg>
                Full Name *
              </span>
            </label>
            <input
              v-model="editForm.Full_Name"
              type="text"
              required
              class="w-full px-4 py-3 bg-white/80 backdrop-blur-sm border-2 border-purple-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all shadow-sm hover:shadow-md"
              placeholder="Enter full name"
            />
          </div>

          <!-- Email -->
          <div class="relative">
            <label class="block text-sm font-bold text-gray-800 mb-2">
              <span class="flex items-center gap-2">
                <svg class="w-4 h-4 text-purple-500" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                  <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                </svg>
                Email *
              </span>
            </label>
            <input
              v-model="editForm.Email"
              type="email"
              required
              class="w-full px-4 py-3 bg-white/80 backdrop-blur-sm border-2 border-purple-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all shadow-sm hover:shadow-md"
              placeholder="Enter email"
            />
          </div>

          <!-- Phone -->
          <div class="relative">
            <label class="block text-sm font-bold text-gray-800 mb-2">
              <span class="flex items-center gap-2">
                <svg class="w-4 h-4 text-purple-500" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z" />
                </svg>
                Phone *
              </span>
            </label>
            <input
              v-model="editForm.Phone"
              type="tel"
              required
              pattern="[0-9]{10}"
              class="w-full px-4 py-3 bg-white/80 backdrop-blur-sm border-2 border-purple-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all shadow-sm hover:shadow-md"
              placeholder="Enter 10-digit phone number"
            />
          </div>

          <!-- DOB and Gender in Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <!-- DOB -->
            <div class="relative">
              <label class="block text-sm font-bold text-gray-800 mb-2">
                <span class="flex items-center gap-2">
                  <svg class="w-4 h-4 text-purple-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd" />
                  </svg>
                  Date of Birth *
                </span>
              </label>
              <input
                v-model="editForm.DOB"
                type="date"
                required
                class="w-full px-4 py-3 bg-white/80 backdrop-blur-sm border-2 border-purple-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all shadow-sm hover:shadow-md"
              />
            </div>

            <!-- Gender -->
            <div class="relative">
              <label class="block text-sm font-bold text-gray-800 mb-2">
                <span class="flex items-center gap-2">
                  <svg class="w-4 h-4 text-purple-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                  </svg>
                  Gender *
                </span>
              </label>
              <select
                v-model="editForm.Gender"
                required
                class="w-full px-4 py-3 bg-white/80 backdrop-blur-sm border-2 border-purple-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all shadow-sm hover:shadow-md"
              >
                <option value="">Select Gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>
          </div>

          <!-- Address -->
          <div class="relative">
            <label class="block text-sm font-bold text-gray-800 mb-2">
              <span class="flex items-center gap-2">
                <svg class="w-4 h-4 text-purple-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
                </svg>
                Address
              </span>
            </label>
            <textarea
              v-model="editForm.Address"
              rows="3"
              class="w-full px-4 py-3 bg-white/80 backdrop-blur-sm border-2 border-purple-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all shadow-sm hover:shadow-md resize-none"
              placeholder="Enter address"
            ></textarea>
          </div>

          <!-- Action Buttons -->
          <div class="flex gap-4 mt-8 pt-4">
            <button
              type="button"
              @click="closeEditModal"
              class="flex-1 bg-white hover:bg-gray-50 text-gray-700 font-bold px-6 py-3.5 rounded-xl shadow-md hover:shadow-lg transition-all border-2 border-gray-300 hover:border-gray-400"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="flex-1 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-bold px-6 py-3.5 rounded-xl shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
            >
              Update Student
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Confirmation Modal -->
    <ConfirmationModal
      :is-open="showConfirmModal"
      :title="confirmModalConfig.title"
      :message="confirmModalConfig.message"
      :variant="confirmModalConfig.variant"
      @confirm="confirmModalConfig.onConfirm"
      @close="showConfirmModal = false"
    />

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "@/utils/axiosInstance";
import AddApplicantsPage from "../AddApplicantsPage.vue";
import UploadStudents from "../UploadStudents.vue";
import ConfirmationModal from "@/components/ConfirmationModal.vue";

const emit = defineEmits(["toast"]);
const router = useRouter();

const applicantsList = ref([]);
const selectedApplicants = ref([]);
const showViewModal = ref(false);
const selectedApplicant = ref(null);
const showAddApplicantPage = ref(false);
const showUploadPage = ref(false);
const filterMode = ref('active'); // 'active', 'all', or 'inactive'
const searchQuery = ref("");

// Edit Modal State
const showEditModal = ref(false);
const editForm = ref({
  Applicant_Id: null,
  Full_Name: '',
  Email: '',
  Phone: '',
  DOB: '',
  Gender: '',
  Address: ''
});

// Confirmation Modal State
const showConfirmModal = ref(false);
const confirmModalConfig = ref({
  title: '',
  message: '',
  variant: 'default',
  onConfirm: null
});

const filteredApplicants = computed(() => {
  // First filter by active/disabled status based on filterMode
  let filtered;
  if (filterMode.value === 'active') {
    filtered = applicantsList.value.filter(a => Number(a.Is_Active) === 1);
  } else if (filterMode.value === 'inactive') {
    filtered = applicantsList.value.filter(a => Number(a.Is_Active) === 0);
  } else {
    // 'all' mode
    filtered = applicantsList.value;
  }
  
  // Then filter by search query
  if (!searchQuery.value.trim()) {
    return filtered;
  }
  
  const query = searchQuery.value.toLowerCase();
  return filtered.filter(a =>
    a.Full_Name?.toLowerCase().includes(query) ||
    a.Email?.toLowerCase().includes(query) ||
    a.Phone?.toLowerCase().includes(query) ||
    String(a.Applicant_Id || '').includes(query)
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

// Edit
const openEditModal = (applicant) => {
  editForm.value = {
    Applicant_Id: applicant.Applicant_Id,
    Full_Name: applicant.Full_Name,
    Email: applicant.Email,
    Phone: applicant.Phone,
    DOB: applicant.DOB ? new Date(applicant.DOB).toISOString().split('T')[0] : '',
    Gender: applicant.Gender,
    Address: applicant.Address || ''
  };
  showEditModal.value = true;
};

const closeEditModal = () => {
  showEditModal.value = false;
  editForm.value = {
    Applicant_Id: null,
    Full_Name: '',
    Email: '',
    Phone: '',
    DOB: '',
    Gender: '',
    Address: ''
  };
};

const updateApplicant = async () => {
  try {
    await axios.put(`/admin/applicants/${editForm.value.Applicant_Id}`, editForm.value);
    emit("toast", {
      message: "Student updated successfully",
      type: "success"
    });
    closeEditModal();
    fetchApplicants();
  } catch (err) {
    emit("toast", {
      message: err.response?.data?.error || "Failed to update student",
      type: "error"
    });
  }
};

// Enable/Disable
const toggleApplicantStatus = (applicant) => {
  const action = applicant.Is_Active === 1 ? "disable" : "enable";
  
  confirmModalConfig.value = {
    title: `${action.charAt(0).toUpperCase() + action.slice(1)} Student`,
    message: `Are you sure you want to ${action} this student?`,
    variant: action === 'disable' ? 'danger' : 'default',
    onConfirm: async () => {
      try {
        await axios.put(`/admin/applicants/toggle-status/${applicant.Applicant_Id}`);
        emit("toast", {
          message: `Student ${action}d successfully`,
          type: "success"
        });
        fetchApplicants();
      } catch (err) {
        emit("toast", {
          message: `Failed to ${action} student`,
          type: "error"
        });
      }
    }
  };
  
  showConfirmModal.value = true;
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