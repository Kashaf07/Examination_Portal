<template>
  <div class="fixed inset-0 backdrop-blur-lg flex items-center justify-center z-50" @keydown="handleKeydown">
    <div class="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full mx-4 transform transition-all duration-300 scale-100">
      <!-- Icon and Title -->
      <div class="text-center mb-6">
        <div class="mx-auto w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mb-4">
          <svg class="w-8 h-8 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
          </svg>
        </div>
        <h3 class="text-2xl font-bold text-gray-900 mb-2">Confirm Submission</h3>
        <p class="text-gray-600 text-lg">Are you sure you want to submit your exam?</p>
      </div>

      <!-- Warning Message -->
      <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
        <p class="text-yellow-800 text-sm font-medium">
          ⚠️ Once submitted, you cannot make any changes to your answers.
        </p>
      </div>

      <!-- Action Buttons -->
      <div class="flex gap-4">
        <button 
          ref="cancelButton"
          @click="$emit('cancel')"
          :class="[
            'flex-1 px-6 py-3 border rounded-lg font-semibold transition-all duration-200 focus:outline-none',
            focusedButton === 'cancel' 
              ? 'border-gray-400 bg-gray-100 text-gray-800 ring-2 ring-gray-300' 
              : 'border-gray-300 text-gray-700 hover:bg-gray-50 hover:border-gray-400'
          ]"
        >
          Cancel
        </button>
        <button 
          ref="confirmButton"
          @click="$emit('confirm')"
          :class="[
            'flex-1 px-6 py-3 rounded-lg font-semibold shadow-lg transition-all duration-200 focus:outline-none',
            focusedButton === 'confirm'
              ? 'bg-gradient-to-r from-purple-700 to-pink-600 text-white ring-2 ring-purple-300 transform -translate-y-0.5 shadow-xl'
              : 'bg-gradient-to-r from-purple-600 to-pink-500 hover:from-purple-700 hover:to-pink-600 text-white hover:shadow-xl hover:-translate-y-0.5'
          ]"
        >
          Submit Exam
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const emit = defineEmits(['confirm', 'cancel'])

const focusedButton = ref('confirm') // Default focus on confirm button
const cancelButton = ref(null)
const confirmButton = ref(null)

const handleKeydown = (event) => {
  if (event.key === 'Enter') {
    event.preventDefault()
    if (focusedButton.value === 'confirm') {
      emit('confirm')
    } else {
      emit('cancel')
    }
  } else if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
    event.preventDefault()
    focusedButton.value = focusedButton.value === 'confirm' ? 'cancel' : 'confirm'
  } else if (event.key === 'Escape') {
    event.preventDefault()
    emit('cancel')
  }
}

onMounted(() => {
  // Focus the modal container for keyboard events
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>