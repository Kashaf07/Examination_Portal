<template>
  <div class="space-y-6">

    <div class="bg-white/80 backdrop-blur-sm shadow-xl rounded-2xl p-8 border border-white/20">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Login Logs</h2>

      <!-- ----------- Logs Table ----------- -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gradient-to-r from-blue-50 to-blue-100 border-b border-blue-200">
              <tr>
                <th class="py-4 px-6 text-left font-semibold text-blue-900">ID</th>
                <th class="py-4 px-6 text-left font-semibold text-blue-900">User Email</th>
                <th class="py-4 px-6 text-left font-semibold text-blue-900">Role</th>
                <th class="py-4 px-6 text-left font-semibold text-blue-900">Login Time</th>
                <th class="py-4 px-6 text-left font-semibold text-blue-900">Logout Time</th>
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
                <td class="py-4 px-6">{{ log.User_Email }}</td>

                <td class="py-4 px-6">
                  <span
                    :class="getRoleBadge(log.Role)"
                    class="px-3 py-1 rounded-full text-xs font-medium"
                  >
                    {{ log.Role }}
                  </span>
                </td>

                <td class="py-4 px-6">{{ formatDateTime(log.Login_Time) }}</td>
                <td class="py-4 px-6">{{ formatDateTime(log.Logout_Time) }}</td>

                <td class="py-4 px-6">
                  <button
                    @click="openViewModal(log)"
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

    <!-- ----------- View Log Modal ----------- -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black/60 backdrop-blur-md flex items-center justify-center z-[9999] p-4"
    >
      <div class="bg-white shadow-2xl rounded-3xl p-8 w-full max-w-md">

        <h3 class="text-2xl font-bold text-gray-800 mb-8 text-center">Login Log Details</h3>

        <div v-if="selectedLog" class="space-y-4">
          <DetailRow label="Log ID" :value="selectedLog.Log_ID" />
          <DetailRow label="User Email" :value="selectedLog.User_Email" />
          <DetailRow label="Role" :value="selectedLog.Role" />
          <DetailRow label="Login Time" :value="formatDateTime(selectedLog.Login_Time)" />
          <DetailRow label="Logout Time" :value="formatDateTime(selectedLog.Logout_Time)" />

          <DetailRow v-if="selectedLog.Student_ID" label="Student ID" :value="selectedLog.Student_ID" />
          <DetailRow v-if="selectedLog.Student_Name" label="Student Name" :value="selectedLog.Student_Name" />
          <DetailRow v-if="selectedLog.Applicant_ID" label="Applicant ID" :value="selectedLog.Applicant_ID" />
        </div>

        <div class="flex justify-center mt-8">
          <button
            @click="closeModal"
            class="px-8 py-3 bg-gray-200 text-gray-700 rounded-full hover:bg-gray-300 transition hover:scale-105"
          >
            Close
          </button>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

// Emit toast to parent
const emit = defineEmits(["toast"]);

// ------------------- Reusable Detail Row Component -------------------
const DetailRow = {
  props: ["label", "value"],
  template: `
    <div class="flex justify-between border-b py-2">
      <span class="font-semibold text-gray-700">{{ label }}:</span>
      <span class="text-gray-800">{{ value }}</span>
    </div>
  `
};

// ------------------- DATA -------------------
const API = "http://localhost:5000/api";

const logs = ref([]);
const showModal = ref(false);
const selectedLog = ref(null);

// ------------------- FETCH LOGS -------------------
const fetchLogs = async () => {
  try {
    const res = await axios.get(`${API}/admin/logs`);
    logs.value = res.data;
  } catch {
    emit("toast", { message: "Error fetching logs", type: "error" });
  }
};

// ------------------- VIEW LOG -------------------
const openViewModal = (log) => {
  selectedLog.value = log;
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

// ------------------- ROLE BADGES -------------------
const getRoleBadge = (role) => {
  switch (role) {
    case "Admin":
      return "bg-purple-100 text-purple-800";
    case "Faculty":
      return "bg-blue-100 text-blue-800";
    case "Student":
      return "bg-green-100 text-green-800";
    default:
      return "bg-gray-100 text-gray-800";
  }
};

// ------------------- DATE FORMAT -------------------
const formatDateTime = (dt) => {
  if (!dt) return "N/A";
  const date = new Date(dt.includes("T") ? dt : dt.replace(" ", "T"));
  return isNaN(date.getTime())
    ? "Invalid"
    : date.toLocaleString("en-IN", { timeZone: "Asia/Kolkata" });
};

onMounted(fetchLogs);
</script>
