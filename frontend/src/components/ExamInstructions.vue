<template>
  <div class="max-w-4xl w-full mx-4 bg-white p-8 rounded-2xl shadow-2xl border border-indigo-100 mt-4 z-10">
    <div class="text-center mb-8">
      <h2 class="text-3xl font-bold text-indigo-700 tracking-tight mb-2">{{ exam.Exam_Name }}</h2>
      <div class="w-20 h-1 bg-gradient-to-r from-indigo-400 to-pink-500 mx-auto rounded-full"></div>
    </div>
    
    <!-- Exam Details Card -->
    <div class="grid grid-cols-2 gap-4 text-lg bg-indigo-50 p-6 rounded-xl mb-8 shadow-sm border border-indigo-100">
      <div class="flex items-center text-gray-800">
        <span class="mr-2 text-indigo-600">🗓</span>
        <strong class="mr-1">Date:</strong> {{ exam.Exam_Date }}
      </div>
      <div class="flex items-center text-gray-800">
        <span class="mr-2 text-indigo-600">🕔</span>
        <strong class="mr-1">Time:</strong> {{ exam.Exam_Time }}
      </div>
      <div class="flex items-center text-gray-800">
        <span class="mr-2 text-indigo-600">⏱</span>
        <strong class="mr-1">Duration:</strong> {{ exam.Duration_Minutes }} mins
      </div>
      <div class="flex items-center text-gray-800">
        <span class="mr-2 text-indigo-600">📝</span>
        <strong class="mr-1">Questions:</strong> {{ questionsCount }}
      </div>
    </div>
    
    <!-- Instructions Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
      <!-- How to Attempt Section -->
      <div class="bg-blue-50 border-l-4 border-blue-400 p-5 rounded-lg shadow">
        <h3 class="font-bold text-blue-800 mb-3 flex items-center text-lg">
          <span class="mr-2">📋</span> How to Attempt
        </h3>
        <ul class="list-disc list-inside text-gray-700 space-y-2 pl-2">
          <li>Read each question carefully before answering</li>
          <li>For MCQ/TF: Select one option using mouse or keyboard arrows</li>
          <li>For Fill/OneWord: Type your answer in the text box</li>
          <li>Use the question navigator to jump between questions</li>
          <li>Answer all questions before submitting</li>
        </ul>
      </div>
      
      <!-- Restrictions Section -->
      <div class="bg-red-50 border-l-4 border-red-400 p-5 rounded-lg shadow">
        <h3 class="font-bold text-red-800 mb-3 flex items-center text-lg">
          <span class="mr-2">🚫</span> Restrictions
        </h3>
        <ul class="list-disc list-inside text-gray-700 space-y-2 pl-2">
          <li>Strictly no page refresh/reload allowed</li>
          <li>No switching tabs/windows (2 attempts max)</li>
          <li>No right-click, copy/paste allowed</li>
          <li>No developer tools access (F12/Ctrl+Shift+I)</li>
          <li>Must remain in fullscreen mode</li>
          <li>Exam will auto-submit when time ends</li>
          <li>Violations may force-submit your exam</li>
        </ul>
      </div>
    </div>
    
    <!-- Confirmation Buttons -->
    <div class="flex justify-between items-center mt-6 pt-5 border-t border-gray-200">
      <button 
        @click="$emit('go-back')" 
        class="flex items-center bg-gray-100 hover:bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-semibold transition-all duration-200 shadow"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
        </svg>
        Cancel
      </button>
      <button 
        @click="$emit('start-exam')" 
        class="flex items-center bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white px-8 py-3 rounded-lg font-bold shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-0.5"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
        </svg>
        Start Exam Now
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  exam: {
    type: Object,
    required: true
  },
  questionsCount: {
    type: Number,
    required: true
  }
})

defineEmits(['go-back', 'start-exam'])
</script>