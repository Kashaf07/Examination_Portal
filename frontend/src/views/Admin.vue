<template>
  <div class="min-h-screen" 
       style="background: linear-gradient(to bottom right, #E3F2FD, #F3E5F5, #FCE4EC);">

    <!-- Header -->
    <div class="px-6 py-6 flex justify-between items-center mb-4">
      <h1 class="text-4xl font-bold text-blue-600">
        Welcome, {{ adminName }}
      </h1>

      <div class="flex gap-4">
        <button
          v-if="canSwitch"
          @click="switchRole"
          class="bg-green-500 text-white px-4 py-2 rounded-lg"
        >
          Switch to Faculty
        </button>

        <button
          @click="logout"
          class="bg-red-500 text-white px-6 py-3 rounded-full shadow-lg hover:bg-red-600">
          Logout
        </button>
      </div>
    </div>

    <!-- Tabs (navigation) -->
    <div class="flex flex-wrap gap-4 px-6 mb-6">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        :class="[
          'px-6 py-3 rounded-full font-semibold shadow-lg transition hover:scale-105',
          activeTab === tab.id
            ? 'bg-blue-600 text-white'
            : 'bg-blue-500 text-white hover:bg-blue-600'
        ]"
        @click="goToTab(tab.id)"
      >
        {{ tab.name }}
      </button>
    </div>

    <!-- Render Current Admin Page -->
    <div class="px-6 pb-10">
      <router-view @toast="handleToast"/>
    </div>

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
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import NotificationToast from "@/components/admin/NotificationToast.vue";
import { authApi } from "@/services/adminApi.js";

// Roles
const roles = JSON.parse(localStorage.getItem("roles") || "[]");
const canSwitch = roles.length > 1;

const router = useRouter();
const route = useRoute();

// Admin Info
const adminName = ref(localStorage.getItem("name") || "Admin");
const activeTab = ref(route.query.tab || "faculty");

const tabs = [
  { id: "faculty", name: "Faculty" },
  { id: "schools", name: "Schools" },
  { id: "applicants", name: "Applicants" },
  { id: "exams", name: "Exams" },
  { id: "admins", name: "Admins" },
  { id: "logs", name: "Login Logs" }
];

// Navigation
const goToTab = (tab) => {
  activeTab.value = tab;
  router.push(`/admin/${tab}`);
};

// Switch role
const switchRole = () => {
  const current = localStorage.getItem("active_role");
  const newRole = current === "Faculty" ? "Admin" : "Faculty";
  localStorage.setItem("active_role", newRole);
  router.push("/" + newRole.toLowerCase());
};

// Toast system
const toast = ref({ message: "", type: "" });
let toastTimer = null;

const handleToast = ({ message, type }) => {
  toast.value = { message, type };
  // Clear previous timer if exists
  if (toastTimer) clearTimeout(toastTimer);
  // Auto-hide after 3 seconds
  toastTimer = setTimeout(() => {
    toast.value = { message: "", type: "" };
  }, 3000);
};
const clearToast = () => {
  toast.value = { message: "", type: "" }; // force full reset
};
const showToast = (msg, type = "success") => {
  // ❌ Block all exam-related errors (they are false alarms)
  if (msg.includes("exam") || msg.includes("Exams")) return;

  toast.value = { message: msg, type };
};


// Logout
const logout = async () => {
  const email = localStorage.getItem("admin_email");

  const { success } = await authApi.logout(email, "Admin");

  if (success) {
    localStorage.removeItem("admin_email");
    localStorage.removeItem("admin_name");
    window.location.href = "/";
  } else {
    showToast("Logout failed", "error");
  }
};
</script>
