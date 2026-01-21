<template>
  <div
    class="fixed inset-0 bg-black/60 backdrop-blur-md flex items-center justify-center z-[9999] p-4"
  >
    <div
      class="bg-white shadow-2xl rounded-3xl p-8 w-full max-w-md relative"
    >

      <!-- Title -->
      <h3 class="text-2xl font-bold text-gray-800 mb-8 text-center">
        Upload Applicants File
      </h3>

      <!-- File Upload -->
      <div class="space-y-4">

        <label class="block text-sm font-semibold text-gray-700">
          Select Excel/CSV File
        </label>

        <input
          type="file"
          accept=".xlsx,.xls,.csv"
          @change="handleFile"
          class="w-full p-2 border border-gray-300 rounded-xl cursor-pointer
                bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"
        />

        <!-- Selected File Display -->
        <p v-if="fileName" class="text-sm text-gray-600">
          Selected: <span class="font-semibold">{{ fileName }}</span>
        </p>

      </div>

      <!-- Buttons -->
      <div class="flex justify-center gap-4 mt-8">

        <button
          @click="$emit('close')"
          class="px-8 py-3 bg-gray-200 text-gray-700 rounded-full hover:bg-gray-300 hover:scale-105 transition"
        >
          Cancel
        </button>

        <button
          @click="submitUpload"
          :disabled="!file"
          class="px-8 py-3 bg-blue-600 text-white rounded-full
                 disabled:bg-blue-300 disabled:cursor-not-allowed
                 hover:bg-blue-700 hover:scale-105 transition"
        >
          Upload
        </button>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

defineEmits(["submit", "close"]);

const file = ref(null);
const fileName = ref("");

const handleFile = (e) => {
  const selected = e.target.files[0];
  if (selected) {
    file.value = selected;
    fileName.value = selected.name;
  }
};

const submitUpload = () => {
  if (file.value) {
    const formData = new FormData();
    formData.append("file", file.value);
    // Emit to parent
    emit("submit", formData);
  }
};
</script>
