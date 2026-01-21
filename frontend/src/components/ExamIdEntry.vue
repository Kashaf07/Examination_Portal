<template>
  <div class="flex-grow flex items-center justify-center w-full z-10">
    <div class="max-w-md w-full bg-white p-8 rounded-3xl shadow-2xl border border-indigo-100 flex flex-col items-center justify-center">
      <h2 class="text-3xl font-bold text-center mb-6 text-indigo-700 tracking-tight flex items-center gap-2">
        <span class="inline-block bg-indigo-100 rounded-full p-2 mr-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2a4 4 0 004 4h2a4 4 0 004-4z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
        </span>
        Exam Portal
      </h2>

      <p class="text-center text-base font-bold text-gray-800 mb-5 leading-relaxed px-4 font-sans tracking-wide">
        Please enter your unique Exam ID provided by the examiner. Double-check before submitting. This will start your official attempt.
      </p>

      <!-- Error Message -->
      <div v-if="examIdError" class="w-full mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
        <p class="text-red-700 text-lg font-bold">❌ Unable to Access Exam</p>
        <div v-if="inlineMessage && inlineMessage.type === 'error'" class="mt-2">
          <p class="text-red-600 text-base font-medium">{{ inlineMessage.text }}</p>
        </div>      
      </div>

      <form @submit.prevent="handleSubmit" class="w-full flex flex-col items-center">
        <input 
          v-model="examId" 
          type="text" 
          inputmode="numeric" 
          pattern="[0-9]*"
          class="w-full p-3 border-2 border-indigo-200 rounded-lg mb-5 focus:outline-none focus:ring-2 focus:ring-indigo-300 focus:border-indigo-400 text-lg font-semibold text-indigo-700 placeholder-gray-400 shadow-sm"
          placeholder="Enter Exam ID" 
          autocomplete="off" 
        />
        <button 
          type="submit"
          class="bg-gradient-to-r from-indigo-500 via-pink-500 to-rose-500 text-white px-7 py-3 rounded-lg hover:from-indigo-600 hover:to-rose-600 w-full font-bold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 text-lg tracking-wide"
        >
          Login
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  inlineMessage: Object,
  examIdError: Boolean
})

const emit = defineEmits(['fetch-exam'])

const examId = ref('')

const handleSubmit = () => {
  emit('fetch-exam', examId.value)
}
</script>