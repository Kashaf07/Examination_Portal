<template>
  <div
    class="fixed inset-0 bg-black/60 backdrop-blur-md flex items-center justify-center z-[9999] p-4"
  >
    <div
      class="bg-white shadow-2xl rounded-3xl p-8 w-full max-w-lg relative"
    >
      <!-- Title -->
      <h3 class="text-2xl font-bold text-gray-800 mb-8 text-center">
        {{ isEdit ? "Edit Exam" : "Create Exam" }}
      </h3>

      <!-- Exam Form -->
      <ExamCreateForm
        :form="form"
        :isEdit="isEdit"
        @submit="(data) => $emit('submit', data)"
        @cancel="$emit('close')"
      />
    </div>
  </div>
</template>

<script setup>
import ExamCreateForm from "@/components/admin/ExamCreateForm.vue";

defineProps({
  form: { type: Object, required: true },
  isEdit: { type: Boolean, default: false },
});

defineEmits(["submit", "close"]);
</script>
