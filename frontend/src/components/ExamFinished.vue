<template>
  <div class="w-full h-full flex flex-col items-center justify-center px-4 py-8 z-20">
    <!-- Finish Summary Card -->
    <div 
      :class="[
        'p-10 rounded-2xl shadow-2xl text-center transition-all duration-300 z-20',
        finishMessage.includes('forcibly ended') 
          ? 'max-w-2xl bg-red-50 border-2 border-red-300' 
          : 'max-w-md bg-white border-2 border-green-100'
      ]"
    >
      <div class="mb-6">
        <div 
          :class="[
            'w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6 shadow-lg text-4xl',
            finishMessage.includes('forcibly ended') 
              ? 'bg-red-100 text-red-600' 
              : 'bg-green-100 text-green-600'
          ]"
        >
          {{ finishMessage.includes('forcibly ended') ? '❌' : '✔️' }}
        </div>

        <h2 class="text-3xl font-bold mb-4 whitespace-pre-line text-black">
          {{ finishMessage }}
        </h2>

        <p v-if="finishMessage.includes('forcibly ended')" class="text-xl font-semibold text-black mt-4">
          📩 Please talk to the respective faculty for clarification.
        </p>

        <p class="text-gray-700 mt-4 text-lg">Your attempt has been recorded.</p>
      </div>

      <div class="bg-gray-50 p-5 rounded-xl shadow-md border border-gray-200">
        <p class="text-sm text-gray-600 mb-2 font-medium">Attempt ID:</p>
        <p class="text-2xl font-bold text-indigo-700">{{ attemptId || 'N/A' }}</p>
      </div>
    </div>

    <!-- Redirect Countdown - Fixed Position Bottom Left -->
    <div 
      class="fixed bottom-8 left-8 z-50 bg-yellow-100 border-3 border-yellow-400 text-yellow-900 px-8 py-4 rounded-2xl shadow-2xl text-xl font-bold tracking-wide animate-blink"
    >
      <div class="flex items-center gap-3">
        <span class="text-2xl">⏳</span>
        <span>Redirecting to login page in {{ redirectCountdown }} second<span v-if="redirectCountdown !== 1">s</span>...</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  finishMessage: {
    type: String,
    required: true
  },
  attemptId: {
    type: [Number, String],
    default: null
  },
  redirectCountdown: {
    type: Number,
    required: true
  }
})
</script>

<style scoped>
@keyframes blink {
  0%, 100% { 
    opacity: 1; 
    transform: scale(1); 
  }
  50% { 
    opacity: 0.85; 
    transform: scale(1.02); 
  }
}

.animate-blink {
  animation: blink 1.5s ease-in-out infinite;
}
</style>