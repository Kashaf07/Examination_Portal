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
        <div class="relative">
          <button
            v-if="canSwitch"
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

        <!-- Welcome -->
        <div v-if="activeTab === null" class="flex items-center justify-center min-h-[80vh]">
          <div class="text-center">
            <div class="w-24 h-24 bg-gradient-to-br from-blue-500 to-indigo-600 text-white rounded-full flex items-center justify-center mx-auto text-4xl font-bold shadow-2xl">
              {{ adminInitial }}
            </div>
            <h1 class="text-4xl font-bold mt-6 text-gray-800">Welcome, {{ adminName }}!</h1>
            <p class="text-gray-600 mt-2">Select a menu item to get started</p>
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
import { ref, computed, onMounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import NotificationToast from "@/components/admin/NotificationToast.vue";
import { authApi } from "@/services/adminApi.js";

const roles = JSON.parse(localStorage.getItem("roles") || "[]");
const canSwitch = true;

const router = useRouter();
const route = useRoute();

const adminName = ref(localStorage.getItem("name") || "Admin")
const adminInitial = computed(() => adminName.value.charAt(0).toUpperCase())

const sidebarOpen = ref(true)
const showRoleMenu = ref(false)
const activeTab = ref(null)

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


const tabs = [
  { id: "faculty", name: "Faculty", icon: "faculty" },
  { id: "schools", name: "Schools", icon: "schools" },
  { id: "designations", name: "Designations", icon: "designations" },
  { id: "role-assignment", name: "Role Assignment", icon: "role-assignment" },
  { id: "groups", name: "Groups", icon: "groups" },
  { id: "applicants", name: "Applicants", icon: "applicants" },
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

onMounted(() => {
  activeTab.value = getAdminTabFromPath(route.path)
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