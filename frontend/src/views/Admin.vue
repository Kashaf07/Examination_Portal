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

  <!-- Sidebar Header (ChatGPT Style) -->
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
          <p class="text-xs text-gray-600">
            Administrator
          </p>
        </div>
      </div>

      <button
        @click="sidebarOpen = !sidebarOpen"
        class="w-9 h-9 flex items-center justify-center rounded-lg border-0 text-white hover:bg-blue-700 transition bg-blue-600 shrink-0"
      >
        ☰
      </button>
    </template>

  </div>
</div>

      <!-- Navigation Menu -->
      <nav class="flex-1 py-4 px-3 space-y-1.5">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="goToTab(tab.id)"
          :class="[
            'w-full flex items-center gap-3 px-4 py-2.5 rounded-xl transition-all duration-200 group relative',
            activeTab === tab.id 
              ? 'bg-blue-100 text-blue-700 shadow-sm' 
              : 'hover:bg-white hover:bg-opacity-40 text-gray-700 hover:text-gray-900'
          ]"
        >
          <div class="icon-container">
            <img 
              :src="'/' + tab.icon + '.png'" 
              :alt="tab.name"
              class="icon-image"
            />
          </div>

          <span v-if="sidebarOpen" class="font-semibold text-sm">
            {{ tab.name }}
          </span>
        </button>
      </nav>

      <!-- Bottom Actions -->
      <div class="absolute bottom-0 left-0 right-0 p-3 border-t border-white border-opacity-30 space-y-2">
        <!-- Switch Role Button -->
        <div class="relative">
          <button
            v-if="canSwitch"
            @click="toggleRoleMenu"
            :class="[
              'w-full flex items-center gap-3 px-4 py-2.5 rounded-xl transition-all duration-200 group',
              'bg-green-500 hover:bg-green-600 text-white shadow-md hover:shadow-lg'
            ]"
          >
            <div class="icon-container">
              <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
              </svg>
            </div>
            <span v-if="sidebarOpen" class="font-semibold text-sm">Switch Role</span>

            <!-- Tooltip for collapsed state -->
            <div
              v-if="!sidebarOpen"
              class="absolute left-full ml-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all whitespace-nowrap z-50"
            >
              Switch Role
            </div>
          </button>

          <!-- Role Dropdown Menu (always positioned to the right) -->
          <div
  v-if="showRoleMenu"
  class="absolute bottom-0 left-full ml-2 bg-white rounded-xl shadow-2xl border border-gray-200 py-3 z-[60] min-w-[280px]"
>
  <div class="px-5 py-3 text-base text-gray-600 border-b border-gray-100">
    Available Roles
  </div>

  <button
    v-for="role in availableRoles"
    :key="role.id"
    @click.stop="selectRole(role.id)"
    :class="[
      'w-full px-5 py-4 text-left text-base hover:bg-blue-50 transition-colors text-gray-700 font-semibold hover:text-blue-600'
    ]"
  >
              <div class="flex items-center justify-between">
                <span>{{ role.name }}</span>
              </div>
            </button>
          </div>
        </div>

        <!-- Logout Button -->
        <button
          @click="logout"
          class="w-full flex items-center gap-3 px-4 py-2.5 rounded-xl bg-red-500 text-white shadow-md hover:bg-red-600"
        >
          Logout
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main 
      :class="[
        'flex-1 transition-all duration-300',
        sidebarOpen ? 'ml-64' : 'ml-20'
      ]"
    >
      <!-- Main Content Area -->
      <div class="px-8 py-6 max-w-full overflow-x-hidden">


        <!-- Welcome/Home Screen (shown when activeTab is 'home' or null) -->
        <!-- In your Admin.vue file, find the welcome section and replace it with this: -->

<!-- Welcome/Home Screen (shown when activeTab is 'home' or null) -->
<div
  v-if="activeTab === null"
  class="flex items-center justify-center min-h-[80vh]"
>
  <div class="text-center">
    <div class="mb-6">
      <div class="w-24 h-24 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center mx-auto shadow-2xl">
        <span class="text-4xl text-white font-bold">{{ adminInitial }}</span>
      </div>
    </div>
    <h1 class="text-4xl font-bold text-gray-800 mb-4">
      Welcome, {{ adminName }}!
    </h1>
    <p class="text-lg text-gray-600">
      Select a menu item from the sidebar to get started
    </p>
  </div>
</div>

        <div v-else>
          <div class="mb-6 mt-2">
  <h1
    class="text-4xl font-bold text-blue-700 leading-tight"
  >
    {{ currentTabName }}
  </h1>
  <p class="text-sm text-gray-600 mt-1">
    Manage your {{ currentTabName.toLowerCase() }} efficiently
  </p>
</div>


          <router-view @toast="handleToast"/>
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
import { ref, computed, onMounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import NotificationToast from "@/components/admin/NotificationToast.vue";
import { authApi } from "@/services/adminApi.js";

const roles = JSON.parse(localStorage.getItem("roles") || "[]");
const canSwitch = roles.length > 1;

const router = useRouter();
const route = useRoute();

const adminName = ref(localStorage.getItem("name") || "Admin");
const adminInitial = computed(() => adminName.value.charAt(0).toUpperCase());

const sidebarOpen = ref(true);
const showRoleMenu = ref(false);
const activeTab = ref(null);


// Tab configuration with PNG icons from public folder - ADDED GROUPS TAB
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
];

const currentTabName = computed(() => {
  const tab = tabs.find(t => t.id === activeTab.value);
  return tab ? tab.name : "Dashboard";
});

// Check if coming from switch role or login
const checkInitialRoute = () => {
  const urlParams = new URLSearchParams(window.location.search);
  const fromSwitch = urlParams.get('from');
  const currentPath = route.path;
  
  console.log('Checking initial route:', { currentPath, fromSwitch });
  
  // CRITICAL: If coming from faculty switch OR at /admin root, show home (blank welcome page)
  if (fromSwitch || currentPath === '/admin' || currentPath === '/admin/') {
    activeTab.value = null;

    // Clean URL - remove query parameters
    if (fromSwitch || window.location.search) {
      window.history.replaceState({}, '', '/admin');
    }
    // Also navigate to /admin route to ensure router is in sync
    if (currentPath !== '/admin') {
      router.replace('/admin');
    }
    return;
  }
  
  // Otherwise, extract the tab from the path
  const pathParts = currentPath.split('/').filter(p => p);
  const lastPart = pathParts[pathParts.length - 1];
  
if (lastPart === 'admin') {
  activeTab.value = null;
  } else if (tabs.find(t => t.id === lastPart)) {
    activeTab.value = lastPart;
  } else {
      activeTab.value = null;
  }
};

// On component mount, check the current route
onMounted(() => {
  checkInitialRoute();
});

// Watch route changes and set active tab
watch(() => route.path, (newPath) => {
  console.log('Route changed to:', newPath);
  
  // Always show home if we're at /admin exactly
  if (newPath === '/admin' || newPath === '/admin/') {
  activeTab.value = null;
  return;
}

  
  // Otherwise, extract the tab from the path
  const pathParts = newPath.split('/').filter(p => p);
  const lastPart = pathParts[pathParts.length - 1];
  
  if (lastPart === 'admin') {
    activeTab.value = null;

  } else if (tabs.find(t => t.id === lastPart)) {
    activeTab.value = lastPart;
  } else {
    activeTab.value = null;
  }
});

// Also watch for URL parameter changes (for switch role)
watch(() => route.query, (newQuery) => {
  if (newQuery.from) {
    console.log('Switched from:', newQuery.from);
    activeTab.value = null;
    // Clean URL
    window.history.replaceState({}, '', '/admin');
    router.replace('/admin');
  }
}, { deep: true });

// Available roles for dropdown
const availableRoles = ref([
  { id: 'faculty', name: 'Faculty' },

]);

// Navigation
const goToTab = (tab) => {
  activeTab.value = tab;
  router.push(`/admin/${tab}`);
};

onMounted(() => {
  const last = route.path.split('/').pop();
  activeTab.value = tabs.find(t => t.id === last) ? last : null;
});

watch(() => route.path, (newPath) => {
  const last = newPath.split('/').pop();
  activeTab.value = tabs.find(t => t.id === last) ? last : null;
});

const toast = ref({ message: "", type: "" });
const handleToast = ({ message, type }) => toast.value = { message, type };
const clearToast = () => toast.value = { message: "", type: "" };

const logout = async () => {
  const email = localStorage.getItem("admin_email");
  const { success } = await authApi.logout(email, "Admin");

  if (success) {
    localStorage.removeItem("admin_email");
    localStorage.removeItem("name");
    localStorage.removeItem("active_role");
    localStorage.removeItem("roles");
    window.location.href = "/";
  }
};
</script>

<style scoped>
/* Prevent all scrolling */
body, html {
  overflow-x: hidden;
  overflow-y: hidden;
}

* {
  box-sizing: border-box;
}

/* Main container - prevent overflow */
.min-h-screen {
  overflow: hidden;
}

/* Icon container for consistent sizing */
.icon-container {
  width: 24px;
  height: 24px;
}
.icon-image {
  width: 24px;
  height: 24px;
  object-fit: contain;
}
</style>
