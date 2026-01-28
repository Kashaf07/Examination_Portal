<template>
  <div class="space-y-6">

    <div class="bg-white/80 backdrop-blur-sm shadow-xl rounded-2xl p-8 border border-white/20">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Login Logs</h2>

      <!-- Logs Table -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gradient-to-r from-blue-50 to-blue-100 border-b border-blue-200">
              <tr>
                <th class="py-4 px-6 text-left font-semibold text-blue-900">ID</th>
                <th class="py-4 px-6 text-left font-semibold text-blue-900">Name</th>
                <th class="py-4 px-6 text-left font-semibold text-blue-900">Email</th>
                <th class="py-4 px-6 text-left font-semibold text-blue-900">Role</th>
                <th class="py-4 px-6 text-left font-semibold text-blue-900">Actions</th>
              </tr>
            </thead>

            <tbody class="bg-white divide-y divide-gray-100">
              <tr
                v-for="(log, i) in logs"
                :key="log.Log_ID"
                class="hover:bg-gray-50 transition"
              >
                <td class="py-4 px-6">{{ i + 1 }}</td>

                <!-- Name -->
                <td class="py-4 px-6">{{ log.User_Name || 'Unknown' }}</td>

                <!-- Email -->
                <td class="py-4 px-6">{{ log.User_Email }}</td>

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
      </div>
    </div>

    <!-- View Logs Modal -->
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

    <!-- User Info Card (clean, no blue background) -->
    <div class="mb-6 text-center">
      <p class="text-gray-600 text-sm">User Email</p>
      <p class="font-semibold text-gray-900 text-lg">{{ selectedUserEmail }}</p>
    </div>

    <!-- History List -->
    <div class="max-h-96 overflow-y-auto space-y-5 pr-2">

      <div
        v-for="(row, index) in userLogs"
        :key="index"
        class="p-5 bg-white rounded-2xl border border-gray-200 shadow hover:shadow-lg transition"
      >

        <!-- LOG HEADER (NO ID SHOWN) -->
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
import { ref, onMounted, getCurrentInstance } from "vue";
import axios from "axios";

const emit = defineEmits(["toast"]);

const API = "http://localhost:5000/api";

const logs = ref([]);
const showModal = ref(false);

const selectedUserEmail = ref("");
const userLogs = ref([]);

// Fetch users (single row each)
const fetchLogs = async () => {
  try {
    const res = await axios.get(`${API}/admin/logs`);
    logs.value = res.data;
  } catch {
    emit("toast", { message: "Error fetching logs", type: "error" });
  }
};

// Fetch full history of selected user
const openViewModal = async (email) => {
  selectedUserEmail.value = email;

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

// Reusable DetailRow
const DetailRow = {
  props: ["label", "value"],
  template: `
    <div class="flex justify-between items-center py-2 px-3 bg-white border rounded-lg shadow-sm">
      <span class="font-semibold text-gray-700">{{ label }}:</span>
      <span class="text-gray-800">{{ value }}</span>
    </div>
  `,
};

// Format Dates
const formatDateTime = (dt) => {
  if (!dt) return "N/A";
  const date = new Date(dt.includes("T") ? dt : dt.replace(" ", "T"));
  return !isNaN(date.getTime())
    ? date.toLocaleString("en-IN", { timeZone: "Asia/Kolkata" })
    : "Invalid";
};

onMounted(fetchLogs);
</script>
