<template>
  <div
    v-if="visible"
    :class="[
      'fixed top-4 right-4 z-[9999] max-w-md transition-opacity duration-300',
      fadingOut ? 'opacity-0' : 'opacity-100'
    ]"
  >
    <div
      :class="[
        'p-4 rounded-xl shadow-2xl border-l-4 transition-all',
        type === 'error'
          ? 'bg-red-50 text-red-800 border-red-500'
          : 'bg-green-50 text-green-800 border-green-500'
      ]"
    >
      <div class="flex justify-between items-center">
        <div class="flex items-center gap-3">

          <!-- Error Icon -->
          <svg
            v-if="type === 'error'"
            class="h-5 w-5 text-red-500"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM7.293 7.293a1 1 0 011.414 0L10 8.586l1.293-1.293a1 1 0 111.414 1.414L11.414 10l1.293 1.293a1 1 0 01-1.414 1.414L10 11.414l-1.293 1.293a1 1 0 01-1.414-1.414L8.586 10 7.293 8.707a1 1 0 010-1.414z"
            />
          </svg>

          <!-- Success Icon -->
          <svg
            v-else
            class="h-5 w-5 text-green-500"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
            />
          </svg>

          <p class="text-sm font-medium">{{ message }}</p>
        </div>

        <button
          @click="closeToast"
          class="text-gray-400 hover:text-gray-600"
        >
          <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
            <path
              fill-rule="evenodd"
              d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 011.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
            />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  message: String,
  type: { type: String, default: "success" }
});

const emit = defineEmits(["clear"]);

// Controls fade-out animation
const fadingOut = ref(false);

// Controls v-if visibility
const visible = ref(true);

// Watch for message appearing / disappearing
watch(
  () => props.message,
  (msg) => {
    if (msg) {
      // Reset to visible when new toast comes
      visible.value = true;
      fadingOut.value = false;
    }
  }
);

// Close handler
const closeToast = () => {
  fadingOut.value = true;

  // Wait for fade-out animation then clear
  setTimeout(() => {
    visible.value = false;
    emit("clear");
  }, 250);
};
</script>
