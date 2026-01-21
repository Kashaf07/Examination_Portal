<template>
  <div class="bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden">
    
    <div class="overflow-x-auto">
      <table class="w-full">
        
        <!-- HEADER -->
        <thead class="bg-gradient-to-r from-blue-50 to-blue-100 border-b border-blue-200">
          <tr>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">ID</th>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">User Email</th>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">Role</th>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">Login Time</th>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">Logout Time</th>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">Actions</th>
          </tr>
        </thead>

        <!-- BODY -->
        <tbody class="bg-white divide-y divide-gray-100">
          <tr
            v-for="(log, idx) in logs"
            :key="log.Log_ID"
            class="hover:bg-gray-50 transition"
          >
            <td class="py-4 px-6 text-gray-700 font-medium">
              {{ idx + 1 }}
            </td>

            <td class="py-4 px-6 text-gray-700">
              {{ log.User_Email }}
            </td>

            <!-- Role Chip -->
            <td class="py-4 px-6">
              <span
                :class="[
                  'px-3 py-1 rounded-full text-xs font-medium',
                  getRoleColor(log.Role)
                ]"
              >
                {{ log.Role }}
              </span>
            </td>

            <td class="py-4 px-6 text-gray-700">
              {{ formatDateTime(log.Login_Time) }}
            </td>

            <td class="py-4 px-6 text-gray-700">
              {{ formatDateTime(log.Logout_Time) }}
            </td>

            <!-- Actions -->
            <td class="py-4 px-6">

              <button
                @click="$emit('view', log)"
                class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg
                       text-sm font-medium transition hover:scale-105 shadow-md"
              >
                View
              </button>

            </td>
          </tr>
        </tbody>

      </table>
    </div>

    <!-- EMPTY STATE -->
    <div
      v-if="logs.length === 0"
      class="text-center py-10 text-gray-500"
    >
      No login logs found.
    </div>

  </div>
</template>

<script setup>
const props = defineProps({
  logs: { type: Array, required: true },
});

const emit = defineEmits(["view"]);

const formatDateTime = (dateString) => {
  if (!dateString) return "N/A";
  const iso = dateString.includes("T") ? dateString : dateString.replace(" ", "T");
  const d = new Date(iso);
  return isNaN(d.getTime())
    ? "Invalid"
    : d.toLocaleString("en-IN", { timeZone: "Asia/Kolkata" });
};

const getRoleColor = (role) => {
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
</script>
