<template>
  <div class="min-h-screen flex" style="background: linear-gradient(to bottom right, #E3F2FD, #F3E5F5, #FCE4EC);">

    <!-- Sidebar -->
    <aside
      :class="[
        'fixed left-0 top-0 h-screen border-r border-gray-200 text-gray-800 transition-all duration-300 z-50 shadow-lg overflow-visible',
        sidebarOpen ? 'w-64' : 'w-20'
      ]"
      style="background: linear-gradient(180deg, #B6D4F2, #DCEBFA);"
    >
      <!-- Sidebar Header -->
      <div class="px-4 py-3 border-b border-white/40">
        <div class="flex items-center justify-between">

          <template v-if="!sidebarOpen">
            <button
              @click="sidebarOpen = !sidebarOpen"
              class="w-10 h-10 flex items-center justify-center rounded-xl
                     bg-gradient-to-br from-blue-500 to-indigo-600
                     text-white shadow-md hover:shadow-lg transition"
            >
              ☰
            </button>
          </template>

          <template v-else>
            <div class="flex items-center gap-3 overflow-hidden">
              <div class="w-9 h-9 bg-gradient-to-br from-blue-500 to-indigo-600 text-white flex items-center justify-center rounded-full font-bold">
                {{ adminInitial }}
              </div>
              <div class="leading-tight truncate">
                <p class="font-semibold text-gray-800 text-sm truncate">
                  {{ adminName }}
                </p>
                <p class="text-xs text-gray-600">Administrator</p>
              </div>
            </div>

            <button
              @click="sidebarOpen = !sidebarOpen"
              class="w-9 h-9 flex items-center justify-center rounded-lg text-white bg-blue-600 hover:bg-blue-700 transition"
            >
              ☰
            </button>
          </template>
        </div>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 py-4 px-3 space-y-1.5 overflow-visible">
        <button
        v-for="tab in tabs"
      :key="tab.id"
      @mouseenter="showTooltip($event, tab.name)"
      @mouseleave="hideTooltip"
      @click="goToTab(tab.id)"
          :class="[
            'w-full flex items-center gap-3 px-4 py-2.5 rounded-xl transition-all duration-200 group relative',
            activeTab === tab.id
              ? 'bg-blue-100 text-blue-700 shadow-sm'
              : 'hover:bg-white hover:bg-opacity-40 text-gray-700'
          ]"
        >
          <div class="w-6 h-6 flex items-center justify-center shrink-0">
            <img :src="'/' + tab.icon + '.png'" :alt="tab.name" class="w-full h-full object-contain" />
          </div>
          <span v-if="sidebarOpen" class="font-semibold text-sm">{{ tab.name }}</span>
          
          <!-- Tooltip (shows on hover for both collapsed and expanded states) -->
          
        </button>
      </nav>

      <!-- Bottom -->
      <div class="absolute bottom-0 left-0 right-0 p-3 border-t border-white/30 space-y-2">

        <!-- Switch Role -->
        <div class="relative" v-if="canSwitch">
          <button
            @click="toggleRoleMenu"
            :class="[
              'w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl transition-all duration-200 group relative',
              'bg-green-500 hover:bg-green-600 text-white shadow-md hover:shadow-lg'
            ]"
          >
            <!-- Icon (shows in both states) -->
            <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
            </svg>
            
            <!-- Text (only shows when expanded) -->
            <span v-if="sidebarOpen" class="font-semibold text-sm whitespace-nowrap">Switch Role</span>

            <!-- Tooltip (shows on hover for both states) -->
            <div
              class="absolute left-full ml-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all whitespace-nowrap z-50 pointer-events-none"
            >
              Switch Role
            </div>
          </button>

          <!-- Role Dropdown Menu -->
          <div
            v-if="showRoleMenu"
            class="absolute bottom-0 left-full ml-4
       bg-white rounded-2xl
       shadow-xl shadow-black/10
       py-4 z-[60] min-w-[300px]"

          >
            <div class="px-6 pb-3 text-gray-500 text-lg font-medium">
  Available Roles
</div>

            <button
              v-for="role in availableRoles"
              :key="role.id"
              @click.stop="selectRole(role.id)"
              class="w-full px-5 py-4 text-left hover:bg-blue-50 font-semibold text-gray-700 hover:text-blue-600 transition-colors"
            >
              {{ role.name }}
            </button>
          </div>
        </div>

        <!-- Logout -->
        <button
          @click="logout"
          :class="[
            'w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl transition-all duration-200 group relative',
            'bg-red-500 hover:bg-red-600 text-white shadow-md hover:shadow-lg'
          ]"
        >
          <!-- Icon (shows in both states) -->
          <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          
          <!-- Text (only shows when expanded) -->
          <span v-if="sidebarOpen" class="font-semibold text-sm">Logout</span>

          <!-- Tooltip (shows on hover for both states) -->
          <div
            class="absolute left-full ml-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all whitespace-nowrap z-50 pointer-events-none"
          >
            Logout
          </div>
        </button>
      </div>
    </aside>

    <!-- Main -->
    <main :class="['flex-1 transition-all duration-300', sidebarOpen ? 'ml-64' : 'ml-20']">
      <div class="px-8 py-6">
     <!-- 🔔 Notification Bell -->
<div class="flex justify-end mb-4">
  <div class="relative" ref="notificationContainer">

    <!-- 🔔 Bell Button -->
    <button
      @click="toggleNotifications"
      aria-label="Admin Notifications"
      class="w-11 h-11 bg-white rounded-full shadow-md
             flex items-center justify-center
             hover:bg-gray-100 relative
             outline-none border-none cursor-pointer"
    >
      🔔
      <span
        v-if="examReminders.length"
        class="absolute -top-1 -right-1 bg-red-600 text-white
               text-xs font-bold rounded-full px-1.5"
      >
        {{ examReminders.length }}
      </span>
    </button>

    <!-- Dropdown -->
    <div
      v-if="showNotifications"
      class="absolute right-0 mt-3 w-[420px]
             bg-white rounded-2xl
             shadow-xl z-[9999]
             overflow-hidden border-none outline-none"
    >
      <!-- Header -->
      <div class="px-6 py-4 bg-gradient-to-r from-indigo-50 to-blue-50
                  flex justify-between items-center">
        <div class="flex items-center gap-2">
          <span class="text-lg">🔔</span>
          <span class="font-bold text-gray-800">
            Admin Exam Notifications
          </span>
        </div>
        <span class="text-sm text-gray-500">
          {{ examReminders.length }}
        </span>
      </div>

      <!-- Notifications -->
      <div
        v-if="examReminders.length"
        class="p-4 space-y-3 max-h-[420px] overflow-y-auto bg-white"
      >
        <div
          v-for="(exam, index) in examReminders"
          :key="exam.Notification_ID"
          class="rounded-xl p-4 bg-gray-50
                 hover:bg-indigo-50 transition
                 relative cursor-default"
        >
          <!-- ❌ Remove -->
          <button
            @click.stop="removeNotification(index)"
            class="absolute top-3 right-3 text-gray-400
                   hover:text-red-500 text-lg font-bold"
            title="Dismiss"
          >
            ×
          </button>

          <!-- Exam Name -->
          <p class="font-semibold text-sm text-gray-800">
            {{ exam.Exam_Name }}
          </p>

          <!-- Meta -->
          <div class="flex flex-wrap gap-3 text-xs text-gray-500 mt-1">
  <span>📅 {{ exam.Exam_Date }}</span>
  <span>⏰ {{ exam.Exam_Time }}</span>

  <span
    v-if="exam.Faculty_Name"
    class="text-indigo-600 font-medium"
  >
    👨‍🏫 {{ exam.Faculty_Name }}
  </span>

  <!-- 🔴 STARTING SOON TAG -->
  <span
    v-if="isStartingSoon(exam)"
    class="bg-red-100 text-red-600 px-2 py-0.5 rounded-full font-semibold"
  >
    ⏳ Starting Soon
  </span>

  <!-- 🟢 COUNTDOWN -->
  <span
    v-if="isStartingSoon(exam)"
    class="text-green-600 font-semibold"
  >
    ⏱ {{ formatCountdown(exam) }}
  </span>
</div>

        </div>
      </div>

      <!-- Empty -->
      <div v-else class="px-6 py-8 text-center text-gray-500">
        <div class="text-3xl mb-2">📭</div>
        No upcoming exams
      </div>
    </div>

  </div>
</div>






        <!-- Dashboard -->
<div v-if="activeTab === null" class="space-y-8">

  <!-- Welcome Card -->
  <div class="bg-white/80 backdrop-blur-lg rounded-2xl p-8 shadow-xl">
    <div class="flex items-center gap-4">
      <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-600
                  text-white rounded-full flex items-center justify-center
                  text-2xl font-bold shadow-xl">
        {{ adminInitial }}
      </div>
      <div>
        <h1 class="text-3xl font-bold text-gray-800">
          Welcome, {{ adminName }}!
        </h1>
        <p class="text-gray-600 mt-1">
          Here's what's coming up 👇
        </p>
      </div>
    </div>
  </div>

  
</div>


        <!-- Routed Content -->
        <div v-else>
          <div class="mb-6">
            <h1 class="text-4xl font-bold text-blue-700 leading-tight">{{ currentTabName }}</h1>
            <p class="text-sm text-gray-600 mt-1">Manage your {{ currentTabName.toLowerCase() }} efficiently</p>
          </div>
          <router-view @toast="handleToast" />
        </div>
      </div>
    </main>

    <NotificationToast
      v-if="toast.message"
      :message="toast.message"
      :type="toast.type"
      @clear="clearToast"
    />
  </div>
  <div
  v-if="tooltip.visible && !sidebarOpen"
  class="fixed px-3 py-2 bg-gray-900 text-white text-sm rounded-lg
         whitespace-nowrap z-[99999] pointer-events-none"
  :style="{
    left: '80px',
    top: tooltip.top + 'px',
    transform: 'translateY(-50%)'
  }"
>
  {{ tooltip.text }}
</div>

</template>


<script setup>
import axios from "axios";
import { ref, computed, onMounted, onUnmounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import NotificationToast from "@/components/admin/NotificationToast.vue";
import { authApi } from "@/services/adminApi.js";

const router = useRouter();
const now = ref(new Date())

const route = useRoute();
const getRemainingMinutes = (exam) => {
  const examDateTime = new Date(`${exam.Exam_Date}T${exam.Exam_Time}`)
  return Math.floor((examDateTime - now.value) / 60000)
}




const isStartingSoon = (exam) => {
  const mins = getRemainingMinutes(exam)
  return mins >= 0 && mins <= 10
}


const formatCountdown = (exam) => {
  const examDateTime = new Date(`${exam.Exam_Date}T${exam.Exam_Time}`)
  const diff = examDateTime - now.value

  if (diff <= 0) return "Starting now"

  const mins = Math.floor(diff / 60000)
  const secs = Math.floor((diff % 60000) / 1000)

  return `${mins}m ${secs}s`
}



const adminName = ref(localStorage.getItem("name") || "Admin")
const adminInitial = computed(() => adminName.value.charAt(0).toUpperCase())
const adminEmail = localStorage.getItem("email")

const sidebarOpen = ref(true)
const showRoleMenu = ref(false)
const activeTab = ref(null)
const canSwitch = ref(false)

const tooltip = ref({
  text: '',
  top: 0,
  visible: false
})

const showTooltip = (event, text) => {
  const rect = event.currentTarget.getBoundingClientRect()
  tooltip.value.text = text
  tooltip.value.top = rect.top + rect.height / 2
  tooltip.value.visible = true
}

const hideTooltip = () => {
  tooltip.value.visible = false
}

/* ================= 🔕 DISMISS SINGLE NOTIFICATION ================= */
const removeNotification = (index) => {
  examReminders.value.splice(index, 1)
}

const tabs = [
  { id: "faculty", name: "Faculty", icon: "faculty" },
  { id: "schools", name: "Schools", icon: "schools" },
  { id: "designations", name: "Designations", icon: "designations" },
  { id: "role-assignment", name: "Role Assignment", icon: "role-assignment" },
  { id: "groups", name: "Groups", icon: "groups" },
  { id: "applicants", name: "Students", icon: "applicants" },
  { id: "exams", name: "Exams", icon: "exams" },
  { id: "admins", name: "Admins", icon: "admins" },
  { id: "logs", name: "Login Logs", icon: "logs" }
]

const currentTabName = computed(() => {
  const tab = tabs.find(t => t.id === activeTab.value)
  return tab ? tab.name : "Dashboard"
})

const getAdminTabFromPath = (path) => {
  const parts = path.split('/').filter(Boolean)
  if (parts[0] === 'admin' && parts[1]) {
    return tabs.find(t => t.id === parts[1]) ? parts[1] : null
  }
  return null
}

// Check if admin can switch to faculty role
const checkFacultyRole = async () => {
  try {
    const response = await axios.get(`http://localhost:5000/api/admin/check-faculty-role/${adminEmail}`)
    if (response.data.success) {
      canSwitch.value = response.data.isFaculty
    }
  } catch (error) {
    console.error("Error checking faculty role:", error)
    canSwitch.value = false
  }
}

// 🔔 Notification state
const showNotifications = ref(false)
const examReminders = ref([])
const notificationContainer = ref(null)

let notificationTimer = null
let countdownTimer = null

/* ================= TOGGLE NOTIFICATIONS ================= */
const toggleNotifications = () => {
  showNotifications.value = !showNotifications.value
}

/* ================= CLICK OUTSIDE TO CLOSE NOTIFICATIONS ================= */
const handleClickOutside = (event) => {
  if (notificationContainer.value && !notificationContainer.value.contains(event.target)) {
    showNotifications.value = false
  }
}

onUnmounted(() => {
  if (notificationTimer) clearInterval(notificationTimer)
  if (countdownTimer) clearInterval(countdownTimer)
  // Remove click outside listener
  document.removeEventListener('click', handleClickOutside)
})


onMounted(() => {
  activeTab.value = getAdminTabFromPath(route.path)
  checkFacultyRole()

  loadExamReminders()

  // 🔁 Refresh notifications every 10s
  notificationTimer = setInterval(() => {
    loadExamReminders()
  }, 10000)

  // ⏱ Update countdown every second (UI only)
  countdownTimer = setInterval(() => {
  now.value = new Date()
}, 1000)

  // Add click outside listener
  document.addEventListener('click', handleClickOutside)

})

watch(() => route.path, (newPath) => {
  activeTab.value = getAdminTabFromPath(newPath)
})

const goToTab = (tab) => {
  activeTab.value = tab
  router.push(`/admin/${tab}`)
}

const availableRoles = ref([{ id: 'faculty', name: 'Faculty' }])
const toggleRoleMenu = () => showRoleMenu.value = !showRoleMenu.value

const selectRole = (roleId) => {
  localStorage.setItem("active_role", "Faculty")
  showRoleMenu.value = false
  router.push('/faculty')
}


// Load exam reminders (ADMIN)
// 🔔 Load ADMIN notifications (FIXED)
const loadExamReminders = async () => {
  try {
    const res = await axios.get(
      "http://localhost:5000/api/admin/notifications"
    )

    if (res.data.success) {
      examReminders.value = res.data.reminders
    }
  } catch (err) {
    console.error("ADMIN NOTIFICATION ERROR:", err)
  }
}


// ADD inside your existing onMounted (do NOT create a new one)
loadExamReminders()

const toast = ref({ message: "", type: "" })
let timer
const handleToast = (data) => {
  toast.value = data
  clearTimeout(timer)
  timer = setTimeout(() => toast.value = { message: "", type: "" }, 3000)
}
const clearToast = () => toast.value = { message: "", type: "" }

const logout = async () => {
  const email = localStorage.getItem("email");

  if (!email) {
    console.error("No email found in localStorage.");
  } else {
    try {
      await axios.post("http://localhost:5000/api/admin/logout", {
        email: email
      });
      console.log("Logout time saved for:", email);
    } catch (error) {
      console.error("Logout logging failed:", error);
    }
  }

  localStorage.clear();
  router.push('/');
};

</script>

<style scoped>
/* Prevent scrolling issues */
body, html {
  overflow-x: hidden;
}

* {
  box-sizing: border-box;
}

/* Hide scrollbar for navigation and main content */
nav::-webkit-scrollbar,
main::-webkit-scrollbar {
  display: none;
}

nav,
main {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

/* Ensure tooltips appear above everything */
.group:hover .absolute {
  z-index: 9999 !important;
}
</style>