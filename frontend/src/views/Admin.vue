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
      <div class="p-8 pt-16 max-w-full overflow-x-hidden"> 

        <div v-if="activeTab === null" class="flex items-center justify-center min-h-[80vh]">
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

        <div v-else>
          <div class="mb-8">
            <h1 class="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
              {{ currentTabName }}
            </h1>
            <p class="text-gray-600 mt-2">
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

/* 🔴 ONLY CHANGE IS HERE 🔴 */
const tabs = [
  { id: "faculty", name: "Faculty", icon: "faculty" },

  // ✅ ADDED FOR FACULTY GROUPS
  { id: "faculty-groups", name: "Faculty Groups", icon: "faculty" },

  { id: "schools", name: "Schools", icon: "schools" },
  { id: "applicants", name: "Applicants", icon: "applicants" },
  { id: "exams", name: "Exams", icon: "exams" },
  { id: "admins", name: "Admins", icon: "admins" },
  { id: "logs", name: "Login Logs", icon: "logs" }
];

const currentTabName = computed(() => {
  const tab = tabs.find(t => t.id === activeTab.value);
  return tab ? tab.name : "Dashboard";
});

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
    localStorage.clear();
    window.location.href = "/";
  }
};
</script>

<style scoped>
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
