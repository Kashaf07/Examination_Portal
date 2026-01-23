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

    <!-- When Closed: Show Avatar on Left, Hamburger on Right -->
    <template v-if="!sidebarOpen">
  <button
    @click="sidebarOpen = !sidebarOpen"
    class="w-10 h-10 flex items-center justify-center rounded-xl
           bg-gradient-to-br from-blue-500 to-indigo-600
           text-white shadow-md hover:shadow-lg transition"
    title="Open Menu"
  >
    <svg
      class="w-6 h-6"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
      stroke-width="2"
      stroke-linecap="round"
    >
      <line x1="4" y1="6" x2="20" y2="6" />
      <line x1="4" y1="12" x2="20" y2="12" />
      <line x1="4" y1="18" x2="20" y2="18" />
    </svg>
  </button>
</template>


    <!-- When Open: Show Avatar + Name on Left, Hamburger on Right -->
    <template v-else>
      <div class="flex items-center gap-3 overflow-hidden">
        <div class="w-9 h-9 bg-gradient-to-br from-blue-500 to-indigo-600 text-white flex items-center justify-center rounded-full font-bold shrink-0 shadow-md">
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
        <svg
          class="w-5 h-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          stroke-width="2"
        >
          <line x1="4" y1="6" x2="20" y2="6" stroke-linecap="round"/>
          <line x1="4" y1="12" x2="20" y2="12" stroke-linecap="round"/>
          <line x1="4" y1="18" x2="20" y2="18" stroke-linecap="round"/>
        </svg>
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
          <!-- Icon Image -->
          <div class="icon-container">
            <img 
              :src="'/' + tab.icon + '.png'" 
              :alt="tab.name"
              class="icon-image"
            />
          </div>

          
          <!-- Label -->
          <span 
            v-if="sidebarOpen" 
            class="font-semibold text-sm"
          >
            {{ tab.name }}
          </span>

          <!-- Tooltip for collapsed state -->
          <div
            v-if="!sidebarOpen"
            class="absolute left-full ml-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all whitespace-nowrap z-50"
          >
            {{ tab.name }}
          </div>
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
            class="absolute bottom-0 left-full ml-2 bg-white rounded-xl shadow-2xl border border-gray-200 py-2 z-[60] min-w-[240px]"
          >
            <div class="px-4 py-2 text-sm font-bold text-gray-700 border-b border-gray-100">
              Available Roles
            </div>

            <button
              v-for="role in availableRoles"
              :key="role.id"
              @click.stop="selectRole(role.id)"
              :class="[
                'w-full px-4 py-3 text-left text-sm hover:bg-blue-50 transition-colors text-gray-700'
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
          :class="[
            'w-full flex items-center gap-3 px-4 py-2.5 rounded-xl transition-all duration-200 group',
            'bg-red-500 hover:bg-red-600 text-white shadow-md hover:shadow-lg relative'
          ]"
        >
          <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          <span v-if="sidebarOpen" class="font-semibold text-sm">Logout</span>

          <!-- Tooltip for collapsed state -->
          <div
            v-if="!sidebarOpen"
            class="absolute left-full ml-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all whitespace-nowrap z-50"
          >
            Logout
          </div>
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
      <div class="p-8 pt-16 max-w-full overflow-x-hidden"> 

        <!-- Welcome/Home Screen (shown when activeTab is 'home' or null) -->
        <div
  v-if="activeTab === null"
  class="flex items-center justify-center min-h-[80vh]"
>

          <div class="text-center">
            <div class="mb-6">
              <div class="w-32 h-32 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center mx-auto shadow-2xl">
                <span class="text-6xl text-white font-bold">{{ adminInitial }}</span>
              </div>
            </div>
            <h1 class="text-6xl font-bold text-gray-800 mb-4">
              Welcome, {{ adminName }}!
            </h1>
            <p class="text-xl text-gray-600">
              Select a menu item from the sidebar to get started
            </p>
          </div>
        </div>

        <!-- Content Area (shown when specific tab is selected) -->
        <div v-else>
          <div class="mb-8">
            <h1 class="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
              {{ currentTabName }}
            </h1>
            <p class="text-gray-600 mt-2">Manage your {{ currentTabName.toLowerCase() }} efficiently</p>
          </div>

          <router-view @toast="handleToast"/>
        </div>
      </div>
    </main>

    <!-- Toast Notification -->
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

// Roles
const roles = JSON.parse(localStorage.getItem("roles") || "[]");
const canSwitch = roles.length > 1;

const router = useRouter();
const route = useRoute();

// Admin Info - Using "name" key like in the first code
const adminName = ref(localStorage.getItem("name") || "Admin");
const adminInitial = computed(() => adminName.value.charAt(0).toUpperCase());

// Sidebar state
const sidebarOpen = ref(true);

// Role menu state
const showRoleMenu = ref(false);

// Active tab detection - Default to 'home' (blank welcome page)
const activeTab = ref(null);


// Tab configuration with PNG icons from public folder
const tabs = [
  { 
    id: "faculty", 
    name: "Faculty", 
    icon: "faculty"  // Will load /faculty.png
  },
  { 
    id: "schools", 
    name: "Schools", 
    icon: "schools"  // Will load /schools.png
  },
  { 
    id: "applicants", 
    name: "Applicants", 
    icon: "applicants"  // Will load /applicants.png
  },
  { 
    id: "exams", 
    name: "Exams", 
    icon: "exams"  // Will load /exams.png
  },
  { 
    id: "admins", 
    name: "Admins", 
    icon: "admins"  // Will load /admins.png
  },
  { 
    id: "logs", 
    name: "Login Logs", 
    icon: "logs"  // Will load /logs.png
  }
];

// Current tab name for header
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
  { id: 'dean', name: 'Dean' },
  { id: 'Head', name: 'Head' },
  { id: 'Program Chair', name: 'Program Chairr' },
  { id: 'Teaching Assistant', name: 'Teaching Assistant' },
]);

// Navigation
const goToTab = (tab) => {
  console.log('Navigating to tab:', tab);
  activeTab.value = tab;
  
  // Navigate to the tab route
  router.push(`/admin/${tab}`);
};

// Toggle role menu
const toggleRoleMenu = () => {
  showRoleMenu.value = !showRoleMenu.value;
};

// Select role - redirects to faculty dashboard directly
const selectRole = (roleId) => {
  if (roleId === 'faculty') {
    // Set active role and navigate to faculty dashboard
    localStorage.setItem("active_role", "Faculty");
    showRoleMenu.value = false;
    router.push('/faculty'); // Navigate to faculty route
  } else {
    // For other roles, just show in console (view only for now)
    console.log(`Role selected: ${roleId} (View only - not implemented yet)`);
    showRoleMenu.value = false;
    handleToast({ 
      message: `${roleId.charAt(0).toUpperCase() + roleId.slice(1)} role - View only (Coming soon)`, 
      type: "info" 
    });
  }
};

// Close role menu when clicking outside
onMounted(() => {
  const handleClickOutside = (e) => {
    if (showRoleMenu.value && !e.target.closest('.relative')) {
      showRoleMenu.value = false;
    }
  };
  
  document.addEventListener('click', handleClickOutside);
  
  // Cleanup
  return () => {
    document.removeEventListener('click', handleClickOutside);
  };
});

// Toast system
const toast = ref({ message: "", type: "" });
let toastTimer = null;

const handleToast = ({ message, type }) => {
  toast.value = { message, type };
  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    toast.value = { message: "", type: "" };
  }, 3000);
};

const clearToast = () => {
  toast.value = { message: "", type: "" };
};

// Logout
const logout = async () => {
  const email = localStorage.getItem("admin_email");
  const { success } = await authApi.logout(email, "Admin");

  if (success) {
    localStorage.removeItem("admin_email");
    localStorage.removeItem("name");  // Changed from "admin_name" to "name"
    localStorage.removeItem("active_role");
    localStorage.removeItem("roles");
    window.location.href = "/";
  } else {
    handleToast({ message: "Logout failed", type: "error" });
  }
};
</script>

<style scoped>
/* Prevent horizontal scroll */
body, html {
  overflow-x: hidden;
}

* {
  box-sizing: border-box;
}

/* Icon container for consistent sizing */
.icon-container {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

/* Icon image styling - standard for dark icons */
.icon-image {
  width: 24px;
  height: 24px;
  object-fit: contain;
  display: block;
}

/* Icon image styling - for white/light icons on colored backgrounds */
.icon-image-white {
  width: 20px;
  height: 20px;
  object-fit: contain;
  display: block;
  filter: brightness(0) invert(1); /* Makes dark icons white */
}
</style>