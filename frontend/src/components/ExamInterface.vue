<template>
  <div class="w-full h-full flex flex-col items-center px-4 py-4">
    <!-- Timer - Top Left Corner -->
    <div class="fixed top-20 left-6 z-40">
      <div class="flex items-center bg-white px-4 py-2 rounded-xl shadow-lg border border-indigo-200">
        <span class="text-xl mr-2">⏳</span>
        <span 
          class="font-mono font-bold text-xl"
          :class="{
            'text-black': timer > 300,
            'text-yellow-800': timer <= 300 && timer > 60,
            'text-red-800': timer <= 60
          }"
        >
          {{ minutes }} : {{ seconds }}
        </span>
      </div>
      
      <div v-if="timer <= 60" class="mt-2 text-sm font-semibold text-center">
        <span class="text-red-700 bg-red-100 px-3 py-1 rounded-lg">🚨 Less than 1 minute!</span>
      </div>
    </div>

    <!-- Question Navigator - Top Right -->
    <div class="fixed top-20 right-6 z-40">
      <div class="grid grid-cols-3 gap-3 bg-white p-4 rounded-xl shadow-lg border border-indigo-200">
        <div
          v-for="(q, idx) in questions"
          :key="idx"
          class="w-10 h-10 flex items-center justify-center rounded-md font-semibold cursor-pointer transition-all duration-200 text-base"
          :class="{
            'bg-indigo-600 text-white shadow-lg scale-110': currentIndex === idx,
            'bg-green-100 text-green-800 border border-green-300': answers[idx] !== null && currentIndex !== idx,
            'bg-gray-100 text-gray-700 hover:bg-indigo-100 hover:text-indigo-700': answers[idx] === null && currentIndex !== idx
          }"
          @click="$emit('jump-to-question', idx)"
        >
          {{ idx + 1 }}
        </div>
      </div>
    </div>

    <!-- Warning Counter - Below Timer -->
    <div v-if="violationCount > 0 && violationCount < 3"
         class="fixed top-36 left-6 z-40">
      <div class="bg-red-600 text-white px-4 py-2 rounded-lg shadow-xl text-sm font-semibold tracking-wide border border-red-700 flex items-center gap-2">
        ⚠️ Warning {{ violationCount }}/3
      </div>
    </div>

    <!-- Main Content Container - Centered -->
    <div class="w-full max-w-4xl flex flex-col items-center mt-8 mb-8 z-10">
      <!-- Exam Heading -->
      <div class="flex flex-col items-center mb-6">
        <h1 class="text-5xl font-extrabold mb-2 tracking-tight text-[#5a32ea] drop-shadow-md">BCA EE</h1>
        <p class="text-xl italic font-semibold text-pink-700 drop-shadow-sm">
          "Your knowledge is your power. Give it your best!"
        </p>
      </div>

      <!-- Question Card -->
      <div class="w-full bg-white rounded-2xl shadow-2xl border border-indigo-100 p-10 flex flex-col gap-6">
        <div>
          <!-- Question Text -->
          <div class="text-2xl font-bold text-black mb-6 drop-shadow-sm">
            <span v-if="currentQuestion.Question_Type === 'Fill'" v-html="formatFillQuestion(currentQuestion.Question_Text)"></span>
            <span v-else>{{ currentQuestion.Question_Text }}</span>
          </div>

          <!-- MCQ Options -->
          <div v-if="currentQuestion.Question_Type === 'MCQ'" class="space-y-5">
            <label 
              v-for="(opt, key) in options" 
              :key="key"
              class="flex items-center space-x-4 p-5 border-2 rounded-lg cursor-pointer transition-all duration-200 shadow-sm"
              :class="{
                'bg-blue-50 border-blue-400 shadow-md scale-105': selectedOption === key,
                'bg-yellow-50 border-yellow-400 shadow-md': keyboardSelectedOption === key && selectedOption !== key,
                'border-gray-200 hover:bg-blue-50 hover:border-blue-300': selectedOption !== key && keyboardSelectedOption !== key
              }"
              @click="$emit('select-option', key)"
            >
              <input 
                type="radio" 
                :value="key" 
                :checked="selectedOption === key"
                class="w-5 h-5 text-indigo-600 focus:ring-indigo-500 accent-indigo-600" 
              />
              <span class="text-lg text-black">
                <span class="font-bold text-black mr-2">{{ key }}.</span>{{ opt }}
              </span>
            </label>
          </div>

          <!-- True/False Options -->
          <div v-else-if="currentQuestion.Question_Type === 'TF'" class="space-y-5">
            <label 
              v-for="(opt, key) in options" 
              :key="key"
              class="flex items-center space-x-4 p-5 border-2 rounded-lg cursor-pointer transition-all duration-200 shadow-sm"
              :class="{
                'bg-blue-50 border-blue-400 shadow-md scale-105': selectedOption === key,
                'bg-yellow-50 border-yellow-400 shadow-md': keyboardSelectedOption === key && selectedOption !== key,
                'border-gray-200 hover:bg-blue-50 hover:border-blue-300': selectedOption !== key && keyboardSelectedOption !== key
              }"
              @click="$emit('select-option', key)"
            >
              <input 
                type="radio" 
                :value="key" 
                :checked="selectedOption === key"
                class="w-5 h-5 text-indigo-600 focus:ring-indigo-500 accent-indigo-600" 
              />
              <span class="text-lg text-black">
                <span class="font-bold text-black mr-2">{{ key }}.</span>{{ opt }}
              </span>
            </label>
          </div>

          <!-- Fill in the Blank -->
          <div v-else-if="currentQuestion.Question_Type === 'Fill'" class="space-y-5">
            <div class="p-5 border-2 border-indigo-200 rounded-lg">
              <label class="block text-lg font-semibold text-gray-700 mb-3">Your Answer:</label>
              <input 
                ref="fillInput"
                :value="textAnswer"
                @input="$emit('update:textAnswer', $event.target.value)"
                type="text"
                class="w-full p-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-300 focus:border-indigo-400 text-lg"
                placeholder="Type your answer here..."
              />
            </div>
          </div>

          <!-- One Word Answer -->
          <div v-else-if="currentQuestion.Question_Type === 'OneWord'" class="space-y-5">
            <div class="p-5 border-2 border-indigo-200 rounded-lg">
              <label class="block text-lg font-semibold text-gray-700 mb-3">Your Answer:</label>
              <input 
                ref="oneWordInput"
                :value="textAnswer"
                @input="$emit('update:textAnswer', $event.target.value)"
                type="text"
                class="w-full p-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-300 focus:border-indigo-400 text-lg"
                placeholder="Type your answer here..."
              />
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex justify-between items-center mt-10">
            <!-- Submit Button (Left) -->
            <div class="flex items-center">
              <button 
                v-if="allAnswersFilled"
                @click="$emit('finish-exam', '✅ All questions submitted!')"
                class="bg-gradient-to-r from-purple-600 to-pink-500 hover:from-purple-700 hover:to-pink-600 text-white px-8 py-3 rounded-lg font-bold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 text-lg tracking-wide transition-all duration-300"
              >
                Submit Exam
              </button>
            </div>
            
            <!-- Inline Messages (Center) -->
            <div class="flex-1 mx-6">
              <div v-if="inlineMessage && inlineMessage.type === 'error'" 
                   class="p-3 bg-red-50 border border-red-200 rounded-lg text-center">
                <p class="text-red-700 text-base font-bold">{{ inlineMessage.text }}</p>
              </div>
              <div v-else-if="inlineMessage && inlineMessage.type === 'success'" 
                   class="p-3 bg-green-50 border border-green-200 rounded-lg text-center">
                <p class="text-green-700 text-base font-bold">{{ inlineMessage.text }}</p>
              </div>
              <div v-else-if="inlineMessage && inlineMessage.type === 'warning'" 
                   class="p-3 rounded-lg border-l-8 border-red-600 bg-red-100 shadow-md">
                <p class="text-red-800 font-semibold text-base tracking-wide">
                  {{ inlineMessage.text }}
                </p>
              </div>
            </div>
            
            <!-- Next Button (Right) -->
            <div class="flex items-center">
              <button 
                @click="$emit('handle-next')"
                class="bg-gradient-to-r from-indigo-500 via-pink-500 to-rose-500 text-white px-8 py-3 rounded-lg hover:from-indigo-600 hover:to-rose-600 transition-all duration-200 font-bold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 text-lg tracking-wide"
              >
                {{ currentIndex + 1 === questions.length ? 'Submit Exam' : 'Next Question' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  timer: Number,
  questions: Array,
  currentIndex: Number,
  currentQuestion: Object,
  selectedOption: String,
  keyboardSelectedOption: String,
  textAnswer: String,
  answers: Array,
  violationCount: Number,
  inlineMessage: Object
})

const emit = defineEmits([
  'jump-to-question',
  'select-option',
  'update:textAnswer',
  'finish-exam',
  'handle-next'
])

const minutes = computed(() => String(Math.floor(props.timer / 60)).padStart(2, '0'))
const seconds = computed(() => String(props.timer % 60).padStart(2, '0'))

const options = computed(() => {
  const type = props.currentQuestion.Question_Type
  if (type === 'TF') {
    return {
      A: props.currentQuestion.Option_A,
      B: props.currentQuestion.Option_B
    }
  } else if (type === 'MCQ') {
    return {
      A: props.currentQuestion.Option_A,
      B: props.currentQuestion.Option_B,
      C: props.currentQuestion.Option_C,
      D: props.currentQuestion.Option_D
    }
  }
  return {}
})

const allAnswersFilled = computed(() => {
  return props.answers.every(ans => ans !== null)
})

const formatFillQuestion = (text) => {
  const value = props.textAnswer || '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
  const safe = value.replace(/</g, '&lt;').replace(/>/g, '&gt;')
  return text.replace(/____+/g, `
    <span class="inline-block border-b-2 border-blue-600 min-w-[120px] px-1 text-center align-baseline text-indigo-800 font-medium tracking-wide">
      ${safe}
    </span>
  `)
}
</script>