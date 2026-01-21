<template>
  <div
    class="fixed inset-0 bg-black/60 backdrop-blur-md flex items-center justify-center z-[9999] p-4"
  >
    <div
      class="bg-white shadow-2xl rounded-3xl p-8 w-full max-w-md relative"
    >
      <!-- Title -->
      <h3 class="text-2xl font-bold text-gray-800 mb-8 text-center">
        Applicant Details
      </h3>

      <!-- Details -->
      <div v-if="applicant" class="space-y-6">

        <DetailRow label="Full Name" :value="applicant.Full_Name" />
        <DetailRow label="Email" :value="applicant.Email" />
        <DetailRow label="Phone" :value="applicant.Phone" />
        <DetailRow label="DOB" :value="formatDate(applicant.DOB)" />
        <DetailRow label="Gender" :value="applicant.Gender" />
        <DetailRow label="Address" :value="applicant.Address" />
        <DetailRow label="Registration Date" :value="formatDate(applicant.Registration_Date)" />

      </div>

      <!-- Close Button -->
      <div class="flex justify-center mt-8">
        <button
          @click="$emit('close')"
          class="px-8 py-3 bg-gray-200 text-gray-700 rounded-full hover:bg-gray-300 hover:scale-105 transition"
        >
          Close
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";

defineProps({
  applicant: { type: Object, required: true }
});

defineEmits(["close"]);

const formatDate = (dateString) => {
  if (!dateString) return "N/A";
  const iso = dateString.includes("T") ? dateString : dateString.replace(" ", "T");
  const d = new Date(iso);
  return isNaN(d.getTime()) ? "Invalid Date" : d.toLocaleDateString("en-IN");
};
</script>

<!-- Reusable small detail component inside same file -->
<script>
export default {
  components: {
    DetailRow: {
      props: ["label", "value"],
      template: `
        <div class="flex justify-between items-center py-2 border-b border-gray-100">
          <span class="font-semibold text-gray-700">{{ label }}:</span>
          <span class="text-gray-800 font-medium">{{ value || 'N/A' }}</span>
        </div>
      `
    }
  }
}
</script>
