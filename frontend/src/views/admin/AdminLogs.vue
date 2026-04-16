<template>
  <div class="space-y-6">

    <div class="bg-white/80 backdrop-blur-sm shadow-xl rounded-2xl p-8 border border-white/20">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Login Logs</h2>

      <!-- Search Box and Role Filter -->
      <div class="mb-6 flex gap-4 items-center">
        <!-- Search Input -->
        <input
          v-model="searchQuery"
          placeholder="🔍 Search by name or role..."
          class="w-full max-w-xs px-4 py-3 rounded-xl border-2 border-black bg-purple-50
                 focus:bg-white focus:ring-2 focus:ring-blue-400 outline-none transition 
                 text-sm font-medium placeholder:text-gray-600"
        />
      </div>

      <!-- Logs Table -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gradient-to-r from-blue-50 to-blue-100 border-b border-blue-200">
              <tr>
                <th class="py-4 px-6 text-left font-semibold text-blue-900">ID</th>
                <th class="py-4 px-6 text-left font-semibold text-blue-900">Name</th>
                <th class="py-4 px-6 text-left font-semibold text-blue-900">Email</th>
                <th class="py-4 px-6 text-left font-semibold text-blue-900 relative">
                  <div class="flex items-center gap-2">
                    <span>Role</span>
                    <svg 
                      @click.stop="toggleRoleFilter"
                      xmlns="http://www.w3.org/2000/svg" 
                      viewBox="0 0 24 24" 
                      fill="currentColor"
                      class="w-5 h-5 cursor-pointer transition"
                      :class="selectedRole ? 'text-blue-600' : 'text-gray-500 hover:text-blue-600'"
                    >
                      <path d="M3 4h18l-7 8v6l-4 2v-8L3 4z"/>
                    </svg>
                  </div>
                </th>
                <th class="py-4 px-6 text-left font-semibold text-blue-900">Actions</th>
              </tr>
            </thead>

            <tbody class="bg-white divide-y divide-gray-100">
              <tr
                v-for="(log, i) in paginatedLogs"
                :key="log.User_Email"
                class="hover:bg-gray-50 transition"
              >
                <td class="py-4 px-6">{{ (currentPage - 1) * itemsPerPage + i + 1 }}</td>

                <!-- Name -->
                <td class="py-4 px-6 font-medium text-gray-900">{{ log.User_Name || 'Unknown' }}</td>

                <!-- Email -->
                <td class="py-4 px-6 text-gray-700">{{ log.User_Email }}</td>

                <!-- Role -->
                <td class="py-4 px-6">
                  <span
                    :class="getRoleBadge(log.Role)"
                    class="px-3 py-1 rounded-full text-xs font-medium"
                  >
                    {{ log.Role }}
                  </span>
                </td>

                <!-- View Action -->
                <td class="py-4 px-6">
                  <button
                    @click="openViewModal(log.User_Email)"
                    class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm transition shadow hover:scale-105"
                  >
                    View
                  </button>
                </td> 
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination Controls -->
        <div class="bg-gray-50 px-6 py-4 border-t border-gray-200">
          <div class="flex items-center justify-between">
            
            <!-- Results Info -->
            <div class="text-sm text-gray-700">
              Showing 
              <span class="font-semibold">{{ startIndex + 1 }}</span>
              to 
              <span class="font-semibold">{{ endIndex }}</span>
              of 
              <span class="font-semibold">{{ totalLogs }}</span>
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

    <!-- Role Filter Popover -->
    <transition name="fade">
      <div
        v-if="showRoleFilter"
        :style="roleFilterStyle"
        class="fixed bg-white shadow-2xl border border-gray-200 rounded-xl p-4 w-64 z-[9999]"
      >
        <h4 class="text-base font-bold text-gray-800 mb-3">Filter by Role</h4>
        
        <div class="space-y-2 mb-3">
          <button
            @click="selectRoleAndClose('Admin')"
            class="w-full px-3 py-2 rounded-lg border-2 font-semibold transition text-center text-sm"
            :class="selectedRole === 'Admin' 
              ? 'bg-purple-600 text-white border-purple-600' 
              : 'bg-white text-purple-600 border-purple-400 hover:bg-purple-50'"
          >
            Admin
          </button>
          
          <button
            @click="selectRoleAndClose('Faculty')"
            class="w-full px-3 py-2 rounded-lg border-2 font-semibold transition text-center text-sm"
            :class="selectedRole === 'Faculty' 
              ? 'bg-blue-600 text-white border-blue-600' 
              : 'bg-white text-blue-600 border-blue-400 hover:bg-blue-50'"
          >
            Faculty
          </button>
          
          <button
            @click="selectRoleAndClose('Student')"
            class="w-full px-3 py-2 rounded-lg border-2 font-semibold transition text-center text-sm"
            :class="selectedRole === 'Student' 
              ? 'bg-green-600 text-white border-green-600' 
              : 'bg-white text-green-600 border-green-400 hover:bg-green-50'"
          >
            Student
          </button>
        </div>

        <div class="flex justify-between pt-2 border-t border-gray-200">
          <button
            @click="applyRoleFilter"
            class="text-xs text-blue-600 font-semibold hover:text-blue-800 transition"
          >
            Apply
          </button>
          <button
            @click="clearRoleFilter"
            class="text-xs text-red-500 font-semibold hover:text-red-700 transition"
          >
            Clear
          </button>
        </div>
      </div>
    </transition>

    <!-- View Logs Modal -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black/60 backdrop-blur-md flex items-center justify-center z-[9999] p-4"
    >
      <div class="bg-white/93 backdrop-blur-xl shadow-2xl rounded-3xl p-8 w-full max-w-2xl border border-gray-100">

        <!-- Modal Title -->
        <h3 class="text-3xl font-bold text-gray-900 mb-6 text-center tracking-tight">
          Login History
        </h3>

        <!-- User Info Card -->
        <div class="mb-6 text-center">
          <p class="text-gray-600 text-sm">User Email</p>
          <p class="font-semibold text-gray-900 text-lg">{{ selectedUserEmail }}</p>
        </div>

        <!-- History List -->
        <div class="max-h-96 overflow-y-auto space-y-5 pr-2">

          <div
            v-for="(row, index) in displayedUserLogs"
            :key="index"
            class="p-5 bg-white rounded-2xl border border-gray-200 shadow hover:shadow-lg transition"
          >

            <!-- LOG HEADER -->
            <div class="flex items-center justify-between mb-4">
              <span class="text-sm font-medium text-gray-500">
                Log Entry
              </span>
            </div>

            <!-- TIME DETAILS -->
            <div class="space-y-3">

              <!-- Login Time -->
              <div class="flex items-start gap-3">
                <div class="w-10 h-10 bg-green-100 text-green-700 rounded-xl flex items-center justify-center text-lg">
                  ⏱
                </div>
                <div>
                  <p class="font-semibold text-gray-700">Login Time</p>
                  <p class="text-gray-900">{{ formatDateTime(row.Login_Time) }}</p>
                </div>
              </div>

              <!-- Logout Time -->
              <div class="flex items-start gap-3">
                <div class="w-10 h-10 bg-red-100 text-red-700 rounded-xl flex items-center justify-center text-lg">
                  🔒
                </div>
                <div>
                  <p class="font-semibold text-gray-700">Logout Time</p>
                  <p class="text-gray-900">{{ formatDateTime(row.Logout_Time) }}</p>
                </div>
              </div>

            </div>

          </div>

          <!-- View More Button (Centered) -->
          <div 
            v-if="!showAllLogs && userLogs.length > initialLogsToShow"
            class="flex justify-center py-4"
          >
            <button
              @click="showAllLogs = true"
              class="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-full font-semibold shadow-lg transition hover:scale-105 flex items-center gap-2"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
              View More ({{ userLogs.length - initialLogsToShow }} more)
            </button>
          </div>

          <!-- Show Less Button (Centered) -->
          <div 
            v-if="showAllLogs && userLogs.length > initialLogsToShow"
            class="flex justify-center py-4"
          >
            <button
              @click="showAllLogs = false; scrollToTop()"
              class="px-8 py-3 bg-gray-500 hover:bg-gray-600 text-white rounded-full font-semibold shadow-lg transition hover:scale-105 flex items-center gap-2"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/>
              </svg>
              Show Less
            </button>
          </div>

        </div>

        <!-- Close Button -->
        <div class="flex justify-center mt-8">
          <button
            @click="closeModal"
            class="px-10 py-3 bg-gray-300 text-gray-800 rounded-full font-semibold shadow hover:bg-gray-400 transition hover:scale-105"
          >
            Close
          </button>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import axios from "axios";

const emit = defineEmits(["toast"]);

const API = `http://${window.location.hostname}:5000/api`;

// Pagination State (for main table)
const logs = ref([]);
const allLogs = ref([]); // Store all raw logs
const currentPage = ref(1);
const itemsPerPage = ref(20);

// Search and Filter State
const searchQuery = ref('');
const showRoleFilter = ref(false);
const selectedRole = ref('');
const roleFilterStyle = ref({});

// Modal State
const showModal = ref(false);
const selectedUserEmail = ref("");
const userLogs = ref([]);
const showAllLogs = ref(false);
const initialLogsToShow = ref(10);

// Group logs by user (unique email) - show only latest login
const groupedLogs = computed(() => {
  const grouped = {};
  
  allLogs.value.forEach(log => {
    const email = log.User_Email;
    if (!grouped[email]) {
      grouped[email] = {
        User_Email: email,
        User_Name: log.User_Name,
        Role: log.Role,
        Latest_Login: log.Login_Time
      };
    } else {
      // Keep the latest login time
      if (new Date(log.Login_Time) > new Date(grouped[email].Latest_Login)) {
        grouped[email].Latest_Login = log.Login_Time;
      }
    }
  });
  
  return Object.values(grouped);
});

// Filter logs based on search query and role filter
const filteredLogs = computed(() => {
  let result = groupedLogs.value;
  
  // Apply search filter
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(log => {
      const name = (log.User_Name || '').toLowerCase();
      const role = (log.Role || '').toLowerCase();
      return name.includes(query) || role.includes(query);
    });
  }
  
  // Apply role filter
  if (selectedRole.value) {
    result = result.filter(log => log.Role === selectedRole.value);
  }
  
  return result;
});

// Computed - Total Logs
const totalLogs = computed(() => filteredLogs.value.length);

// Computed - Total Pages
const totalPages = computed(() => Math.ceil(totalLogs.value / itemsPerPage.value));

// Computed - Paginated Logs
const paginatedLogs = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return filteredLogs.value.slice(start, end);
});

// Computed - Start Index
const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage.value);

// Computed - End Index
const endIndex = computed(() => {
  const end = currentPage.value * itemsPerPage.value;
  return end > totalLogs.value ? totalLogs.value : end;
});

// Computed - Displayed User Logs (with View More logic)
const displayedUserLogs = computed(() => {
  if (showAllLogs.value) {
    return userLogs.value;
  }
  return userLogs.value.slice(0, initialLogsToShow.value);
});

// Computed - Visible Pages (Google-style pagination)
const visiblePages = computed(() => {
  const pages = [];
  const maxVisible = 5; // Show max 5 page numbers
  
  let start = Math.max(2, currentPage.value - 2);
  let end = Math.min(totalPages.value - 1, currentPage.value + 2);
  
  // Adjust if near start
  if (currentPage.value <= 3) {
    end = Math.min(maxVisible, totalPages.value - 1);
    start = 2;
  }
  
  // Adjust if near end
  if (currentPage.value >= totalPages.value - 2) {
    start = Math.max(2, totalPages.value - maxVisible + 1);
    end = totalPages.value - 1;
  }
  
  for (let i = start; i <= end; i++) {
    pages.push(i);
  }
  
  return pages;
});

// Computed - Show First Page
const showFirstPage = computed(() => {
  return totalPages.value > 1 && !visiblePages.value.includes(1);
});

// Computed - Show Last Page
const showLastPage = computed(() => {
  return totalPages.value > 1 && !visiblePages.value.includes(totalPages.value);
});

// Computed - Show Left Ellipsis
const showLeftEllipsis = computed(() => {
  return visiblePages.value.length > 0 && visiblePages.value[0] > 2;
});

// Computed - Show Right Ellipsis
const showRightEllipsis = computed(() => {
  return visiblePages.value.length > 0 && visiblePages.value[visiblePages.value.length - 1] < totalPages.value - 1;
});

// Method - Go to Page
const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
};

// Method - Scroll to Top of Modal
const scrollToTop = () => {
  const scrollContainer = document.querySelector('.max-h-96');
  if (scrollContainer) {
    scrollContainer.scrollTo({ top: 0, behavior: 'smooth' });
  }
};

// Role Filter Methods
const toggleRoleFilter = (event) => {
  showRoleFilter.value = !showRoleFilter.value;
  
  if (showRoleFilter.value) {
    updateFilterPosition(event);
  }
};

const updateFilterPosition = (event) => {
  const svg = event.target.closest('svg');
  if (!svg) return;
  
  const rect = svg.getBoundingClientRect();
  
  roleFilterStyle.value = {
    position: 'fixed',
    top: `${rect.bottom + 8}px`,
    left: `${rect.left - 120}px`
  };
};

const selectRole = (role) => {
  if (selectedRole.value === role) {
    selectedRole.value = '';
  } else {
    selectedRole.value = role;
  }
};

const selectRoleAndClose = (role) => {
  if (selectedRole.value === role) {
    selectedRole.value = '';
  } else {
    selectedRole.value = role;
  }
  // Auto-apply when selecting a role
  applyRoleFilter();
};

const applyRoleFilter = () => {
  showRoleFilter.value = false;
  currentPage.value = 1; // Reset to first page
};

const clearRoleFilter = () => {
  selectedRole.value = '';
  showRoleFilter.value = false;
  currentPage.value = 1;
};

// Update filter position on scroll
const handleScroll = () => {
  if (showRoleFilter.value) {
    showRoleFilter.value = false;
  }
};

// Close filter when clicking outside
const handleClickOutside = (event) => {
  const filterPopup = document.querySelector('.fixed.bg-white.shadow-2xl');
  if (showRoleFilter.value && filterPopup && !filterPopup.contains(event.target)) {
    const filterButton = event.target.closest('button');
    if (!filterButton || !filterButton.querySelector('svg')) {
      showRoleFilter.value = false;
    }
  }
};

// Fetch all logs
const fetchLogs = async () => {
  try {
    const res = await axios.get(`${API}/admin/logs`);
    allLogs.value = res.data;
    logs.value = res.data;
  } catch {
    emit("toast", { message: "Error fetching logs", type: "error" });
  }
};

// Fetch full history of selected user
const openViewModal = async (email) => {
  selectedUserEmail.value = email;
  showAllLogs.value = false; // Reset to show initial 10

  try {
    const res = await axios.get(`${API}/admin/logs/history/${email}`);
    userLogs.value = res.data;
    showModal.value = true;
  } catch {
    emit("toast", { message: "Error fetching user history", type: "error" });
  }
};

const closeModal = () => {
  showModal.value = false;
  showAllLogs.value = false; // Reset for next time
};

// Role Badge Colors
const getRoleBadge = (role) => {
  switch (role) {
    case "Admin": return "bg-purple-100 text-purple-800";
    case "Faculty": return "bg-blue-100 text-blue-800";
    case "Student": return "bg-green-100 text-green-800";
    default: return "bg-gray-100 text-gray-800";
  }
};

// Format Dates
const formatDateTime = (dt) => {
  if (!dt) return "N/A";
  const date = new Date(dt.includes("T") ? dt : dt.replace(" ", "T"));
  return !isNaN(date.getTime())
    ? date.toLocaleString("en-IN", { timeZone: "Asia/Kolkata" })
    : "Invalid";
};

onMounted(() => {
  fetchLogs();
  document.addEventListener('click', handleClickOutside);
  window.addEventListener('scroll', handleScroll);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
  window.removeEventListener('scroll', handleScroll);
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

/* Custom scrollbar for modal */
.max-h-96::-webkit-scrollbar {
  width: 8px;
}

.max-h-96::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.max-h-96::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 10px;
}

.max-h-96::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* Fade transition for filter popup */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>