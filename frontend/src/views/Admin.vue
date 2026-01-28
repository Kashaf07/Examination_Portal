<template>
  <div class="min-h-screen flex" style="background: linear-gradient(to bottom right, #E3F2FD, #F3E5F5, #FCE4EC);">

    <!-- Sidebar -->
    <aside
      :class="[
        'fixed left-0 top-0 h-screen border-r border-gray-200 text-gray-800 transition-all duration-300 z-50 shadow-lg',
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
      <nav class="flex-1 py-4 px-3 space-y-1.5">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="goToTab(tab.id)"
          :class="[
            'w-full flex items-center gap-3 px-4 py-2.5 rounded-xl transition-all duration-200',
            activeTab === tab.id
              ? 'bg-blue-100 text-blue-700 shadow-sm'
              : 'hover:bg-white hover:bg-opacity-40 text-gray-700'
          ]"
        >
          <img :src="'/' + tab.icon + '.png'" class="w-6 h-6" />
          <span v-if="sidebarOpen" class="font-semibold text-sm">{{ tab.name }}</span>
        </button>
      </nav>

      <!-- Bottom -->
      <div class="absolute bottom-0 left-0 right-0 p-3 border-t border-white/30 space-y-2">

        <!-- Switch Role -->
        <div class="relative">
          <button
            v-if="canSwitch"
            @click="toggleRoleMenu"
            class="w-full flex items-center gap-3 px-4 py-2.5 rounded-xl
                   bg-green-500 hover:bg-green-600 text-white shadow-md"
          >
            Switch Role
          </button>

          <div
            v-if="showRoleMenu"
            class="absolute bottom-0 left-full ml-2 bg-white rounded-xl shadow-2xl border py-3 z-50 min-w-[280px]"
          >
            <div class="px-5 py-3 text-gray-600 border-b">Available Roles</div>
            <button
              v-for="role in availableRoles"
              :key="role.id"
              @click.stop="selectRole(role.id)"
              class="w-full px-5 py-4 text-left hover:bg-blue-50 font-semibold"
            >
              {{ role.name }}
            </button>
          </div>
        </div>

        <!-- Logout -->
        <button
          @click="logout"
          class="w-full px-4 py-2.5 rounded-xl bg-red-500 text-white shadow-md hover:bg-red-600"
        >
          Logout
        </button>
      </div>
    </aside>

    <!-- Main -->
    <main :class="['flex-1 transition-all duration-300', sidebarOpen ? 'ml-64' : 'ml-20']">
      <div class="px-8 py-6">

        <!-- Welcome -->
        <div v-if="activeTab === null" class="flex items-center justify-center min-h-[80vh]">
          <div class="text-center">
            <div class="w-24 h-24 bg-blue-600 text-white rounded-full flex items-center justify-center mx-auto text-4xl font-bold">
              {{ adminInitial }}
            </div>
            <h1 class="text-4xl font-bold mt-6">Welcome, {{ adminName }}!</h1>
            <p class="text-gray-600 mt-2">Select a menu item to get started</p>
          </div>
        </div>

        <!-- Routed Content -->
        <div v-else>
          <h1 class="text-4xl font-bold text-blue-700 mb-4">{{ currentTabName }}</h1>
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
</template>

<script setup>
import axios from "axios";
import { ref, computed, onMounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import NotificationToast from "@/components/admin/NotificationToast.vue";
import { authApi } from "@/services/adminApi.js";
const roles = JSON.parse(localStorage.getItem("roles") || "[]");

// Admin should always be allowed to switch
const canSwitch = true;


const router = useRouter();
const route = useRoute();

const adminName = ref(localStorage.getItem("name") || "Admin")
const adminInitial = computed(() => adminName.value.charAt(0).toUpperCase())

const sidebarOpen = ref(true)
const showRoleMenu = ref(false)
const activeTab = ref(null)

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

/* 🔥 FIXED TAB DETECTION */
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

// Switch role (UNCHANGED)
const availableRoles = ref([{ id: 'faculty', name: 'Faculty' }])
const toggleRoleMenu = () => showRoleMenu.value = !showRoleMenu.value

const selectRole = (roleId) => {
  localStorage.setItem("active_role", "Faculty")
  showRoleMenu.value = false
  router.push('/faculty')
}

// Toast
const toast = ref({ message: "", type: "" })
let timer
const handleToast = (data) => {
  toast.value = data
  clearTimeout(timer)
  timer = setTimeout(() => toast.value = { message: "", type: "" }, 3000)
}
const clearToast = () => toast.value = { message: "", type: "" }

// Logout
const logout = async () => {
  // Your login function stores email as `email`
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
