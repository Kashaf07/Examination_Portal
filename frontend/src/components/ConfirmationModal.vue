<template>
  <div
    v-if="isOpen"
    @click.self="handleCancel"
    class="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-[9999] p-4"
  >
    <div
      class="bg-white rounded-2xl shadow-2xl max-w-md w-full p-8 relative transform transition-all animate-fadeIn"
      @click.stop
    >
      <!-- Title -->
      <h2 class="text-2xl font-bold text-black mb-6 text-center">
        {{ title }}
      </h2>

      <!-- Message -->
      <p class="text-base text-gray-600 mb-8 text-center leading-relaxed">
        {{ message }}
      </p>

      <!-- Action Buttons -->
      <div class="flex gap-4 justify-center">
        <button
          @click="handleCancel"
          class="flex-1 px-6 py-3 bg-white text-gray-700 border border-gray-300 rounded-full hover:bg-gray-50 hover:border-gray-400 transition-all duration-300 font-semibold shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95"
        >
          {{ cancelText }}
        </button>
        <button
          @click="handleConfirm"
          class="flex-1 px-6 py-3 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-all duration-300 font-semibold shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95"
        >
          {{ confirmText }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    default: 'Confirm Action'
  },
  message: {
    type: String,
    default: 'Are you sure you want to proceed?'
  },
  confirmText: {
    type: String,
    default: 'OK'
  },
  cancelText: {
    type: String,
    default: 'Cancel'
  },
  variant: {
    type: String,
    default: 'default', // 'default' or 'danger'
    validator: (value) => ['default', 'danger'].includes(value)
  }
})

const emit = defineEmits(['confirm', 'cancel', 'close'])

const handleConfirm = () => {
  emit('confirm')
  emit('close')
}

const handleCancel = () => {
  emit('cancel')
  emit('close')
}
</script>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.2s ease-out;
}
</style>