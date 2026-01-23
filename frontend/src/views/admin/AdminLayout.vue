<template>
  <div
    class="min-h-screen"
    style="background: linear-gradient(to bottom right, #E3F2FD, #F3E5F5, #FCE4EC)"
  >
    <!-- Header -->
    <div class="px-6 py-6">
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-4xl font-bold text-blue-600">Welcome, {{ adminName }}</h1>

        <div class="flex gap-3">
          <button
            v-if="canSwitch"
            @click="switchRole"
            class="bg-green-500 text-white px-4 py-2 rounded-lg"
          >
            Switch to Faculty
          </button>

          <button
            @click="logout"
            class="bg-red-500 hover:bg-red-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all hover:scale-105"
          >
            Logout
          </button>
        </div>
      </div>

      <!-- Navigation Tabs -->
      <div class="flex flex-wrap gap-4 mb-8">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="navigate(tab.id)"
          class="px-6 py-3 rounded-full font-semibold shadow-lg bg-blue-500 hover:bg-blue-600 text-white transition-all duration-200 transform hover:scale-105"

        >
          {{ tab.name }}
        </button>
      </div>

      <!-- Content Area -->
      <div>
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter, useRoute } from "vue-router";

// Router
const router = useRouter();
const route = useRoute();

// Admin info
const adminName = ref(localStorage.getItem("admin_name") ?? "Admin");
const canSwitch = true;


// Switch role
const switchRole = () => {
  localStorage.setItem("active_role", "Faculty");
  localStorage.setItem("role", "faculty");
  router.replace("/faculty/dashboard");
};



// Tabs
const tabs = [
  { id: "faculty", name: "Faculty" },
  { id: "schools", name: "Schools" },
  { id: "applicants", name: "Applicants" },
  { id: "exams", name: "Exams" },
  { id: "admins", name: "Admins" },
  { id: "logs", name: "Login Logs" },
];

// Detect current tab from route
const currentTab = computed(() => route.path.split("/").pop());

// Navigate between pages
const navigate = (tabId) => {
  router.push(`/admin/${tabId}`);
};

// Logout
const logout = async () => {
  const email = localStorage.getItem("admin_email");

  try {
    await fetch("http://localhost:5000/api/auth/logout", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, role: "Admin" }),
    });

    localStorage.removeItem("admin_email");
    localStorage.removeItem("admin_name");
    window.location.href = "/";
  } catch (err) {
    alert("Logout failed!");
  }
};
</script>
