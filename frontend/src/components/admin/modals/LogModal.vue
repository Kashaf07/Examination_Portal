<template>
  <div
    class="fixed inset-0 bg-black/60 backdrop-blur-md flex items-center justify-center z-[9999] p-4"
  >
    <div
      class="bg-white shadow-2xl rounded-3xl p-8 w-full max-w-lg relative"
    >
      <!-- Title -->
      <h3 class="text-2xl font-bold text-gray-800 mb-8 text-center">
        Log Details
      </h3>

      <div v-if="log" class="space-y-6">
        
        <DetailRow label="User Email" :value="log.User_Email" />
        <DetailRow label="Role" :value="log.Role" />

        <DetailRow
          label="Login Time"
          :value="formatDateTime(log.Login_Time)"
        />

        <DetailRow
          label="Logout Time"
          :value="formatDateTime(log.Logout_Time)"
        />

        <DetailRow
          label="IP Address"
          :value="log.IP_Address || 'N/A'"
        />

        <DetailRow
          label="Device Info"
          :value="log.Device_Info || 'N/A'"
        />

      </div>

      <!-- Close Button -->
      <div class="flex justify-center mt-8">
        <button
          @click="$emit('close')"
          class="px-8 py-3 bg-gray-200 text-gray-700 rounded-full
                 hover:bg-gray-300 hover:scale-105 transition"
        >
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  log: { type: Object, required: true },
});

defineEmits(["close"]);

const formatDateTime = (dt) => {
  if (!dt) return "N/A";
  const iso = dt.includes("T") ? dt : dt.replace(" ", "T");
  const d = new Date(iso);
  return isNaN(d.getTime())
    ? "Invalid Date"
    : d.toLocaleString("en-IN", { timeZone: "Asia/Kolkata" });
};
</script>

<!-- Reusable detail row component -->
<script>
export default {
  components: {
    DetailRow: {
      props: ["label", "value"],
      template: `
        <div class="flex justify-between items-center py-2 border-b border-gray-100">
          <span class="font-semibold text-gray-700">{{ label }} :</span>
          <span class="text-gray-800 font-medium">{{ value }}</span>
        </div>
      `,
    },
  },
};
</script>
