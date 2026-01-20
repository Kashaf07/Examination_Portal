<template>
  <div class="absolute top-4 right-6 z-50 group">
    <div class="bg-white px-6 py-3 rounded-2xl shadow-lg border border-indigo-200 text-base font-semibold text-indigo-800 cursor-default transition-all duration-300 hover:shadow-xl hover:scale-105">
      👤 {{ studentName || studentEmail }}
    </div>
    
    <div class="absolute top-full right-0 mt-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 transform translate-y-2 group-hover:translate-y-0">
      <div class="bg-gradient-to-r from-emerald-500 to-teal-600 text-white px-4 py-3 rounded-xl shadow-2xl border border-emerald-300 min-w-max relative">
        <div class="absolute -top-2 right-4 w-4 h-4 bg-emerald-500 transform rotate-45 border-l border-t border-emerald-300"></div>
        
        <div class="relative z-10">
          <div class="text-xs font-medium text-emerald-100 mb-1">📧 Email Address</div>
          <div class="text-sm font-bold text-white tracking-wide">{{ studentEmail }}</div>
        </div>
        
        <div class="absolute inset-0 bg-gradient-to-r from-white/10 to-transparent rounded-xl"></div>
      </div>
    </div>
  </div>



  <div class="min-h-screen flex flex-col items-center py-6 relative bg-gradient-to-br from-[#d2eaf6] via-[#e1f5fe] to-[#e0f7fa] overflow-hidden" style="position:relative;">
    <svg class="absolute bottom-0 left-0 w-full h-48 md:h-64 lg:h-72" viewBox="0 0 1440 320" fill="none" xmlns="http://www.w3.org/2000/svg" style="z-index:0;">
      <path fill="#b3e0f2" d="M0,224L60,202.7C120,181,240,139,360,144C480,149,600,203,720,197.3C840,192,960,128,1080,117.3C1200,107,1320,149,1380,170.7L1440,192V320H0Z"/>
      <path fill="#cbe7f7" fill-opacity="0.7" d="M0,288L60,272C120,256,240,224,360,197.3C480,171,600,149,720,154.7C840,160,960,192,1080,197.3C1200,203,1320,181,1380,170.7L1440,160V320H0Z"/>
      <path fill="#e0f7fa" fill-opacity="0.5" d="M0,320L60,293.3C120,267,240,213,360,197.3C480,181,600,203,720,197.3C840,192,960,160,1080,154.7C1200,149,1320,171,1380,181.3L1440,192V320H0Z"/>
    </svg>

    <div v-if="stage === 'exam'" class="flex flex-col items-center mb-2 z-10">
      <h1 class="text-4xl font-extrabold mb-1 tracking-tight text-[#5a32ea]">BCA EE</h1>

      <p class="text-lg italic font-medium text-pink-700 drop-shadow-sm mb-2">"Your knowledge is your power. Give it your best!"</p>
    </div>
    

    <div v-if="stage === 'exam'" class="z-10">
  <div class="fixed bottom-190 left-7 z-40">
    <span class="text-xl mr-2">⏳</span>
    <span 
      class="font-mono font-bold text-xl px-4 py-2 rounded-xl shadow-md border"
      :class="{
        'text-black bg-white border-indigo-100': timer > 300,
        'text-yellow-800 bg-yellow-100 border-yellow-400 animate-pulse': timer <= 300 && timer > 60,
        'text-red-800 bg-red-100 border-red-400 animate-bounce': timer <= 60
      }"
    >
      {{ minutes }} : {{ seconds }}
    </span>
    
    <div v-if="timer <= 300" class="mt-2 text-sm font-semibold">
      <span v-if="timer > 60" class="text-black-700"></span>
      <span v-else class="text-red-700">🚨 Less than 1 minute!</span>
    </div>
  </div>
      <div class="absolute top-1/2 right-6 transform -translate-y-1/2 z-40">
        <div class="grid grid-cols-3 gap-3 bg-white p-4 rounded-xl shadow-md border border-indigo-100">
          <div
              v-for="(q, idx) in questions"
              :key="idx"
              class="w-10 h-10 flex items-center justify-center rounded-md font-semibold cursor-pointer transition-all duration-200 text-base"
              :class="{
                'bg-indigo-600 text-white shadow-lg scale-110': currentIndex === idx,
                'bg-green-100 text-green-800 border border-green-300': answers[idx] !== null && currentIndex !== idx,
                'bg-gray-100 text-gray-700 hover:bg-indigo-100 hover:text-indigo-700': answers[idx] === null && currentIndex !== idx
              }"
              @click="jumpToQuestion(idx)"
            >
              {{ idx + 1 }}
            </div>

        </div>
      </div>
    </div>
    <div v-if="stage === 'exam' && violationCount > 0 && violationCount <= 2"
     class="fixed bottom-5 left-5 z-50">
  <div class="bg-red-600 text-white px-4 py-2 rounded-lg shadow-xl text-sm font-semibold tracking-wide border border-red-700 flex items-center gap-2">
    ⚠️ Warning {{ violationCount }}/2
  </div>
</div>


    <div v-if="stage === 'enter'" class="flex-grow flex items-center justify-center w-full z-10">
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

<div v-if="examIdError" class="w-full mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
  <p class="text-red-700 text-lg font-bold">❌ Unable to Access Exam</p>
  <div v-if="inlineMessage && inlineMessage.type === 'error'" class="mt-2">
    <p class="text-red-600 text-base font-medium">{{ inlineMessage.text }}</p>
  </div>      
</div>
<div v-if="examIdError" class="w-full mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
  <p class="text-red-700 text-lg font-bold">❌ Unable to Access Exam</p>
  <div v-if="inlineMessage && inlineMessage.type === 'error'" class="mt-2">
    <p class="text-red-600 text-base font-medium">{{ inlineMessage.text }}</p>
  </div>      
</div>

        <form @submit.prevent="fetchExam" class="w-full flex flex-col items-center">
          <input v-model="examId" type="text" inputmode="numeric" pattern="[0-9]*"
            class="w-full p-3 border-2 border-indigo-200 rounded-lg mb-5 focus:outline-none focus:ring-2 focus:ring-indigo-300 focus:border-indigo-400 text-lg font-semibold text-indigo-700 placeholder-gray-400 shadow-sm"
            placeholder="Enter Exam ID" autocomplete="off" />
          <button type="submit"
            class="bg-gradient-to-r from-indigo-500 via-pink-500 to-rose-500 text-white px-7 py-3 rounded-lg hover:from-indigo-600 hover:to-rose-600 w-full font-bold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 text-lg tracking-wide">
            Login
          </button>
        </form>
      </div>
    </div>

    <div v-if="stage === 'instructions'" class="max-w-4xl w-full mx-4 bg-white p-8 rounded-2xl shadow-2xl border border-indigo-100 mt-4 z-10">
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-indigo-700 tracking-tight mb-2">{{ exam.Exam_Name }}</h2>
        <div class="w-20 h-1 bg-gradient-to-r from-indigo-400 to-pink-500 mx-auto rounded-full"></div>
      </div>
      
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
          <strong class="mr-1">Questions:</strong> {{ questions.length }}
        </div>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
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
        
        <div class="bg-red-50 border-l-4 border-red-400 p-5 rounded-lg shadow">
          <h3 class="font-bold text-red-800 mb-3 flex items-center text-lg">
            <span class="mr-2">🚫</span> Restrictions
          </h3>
          <ul class="list-disc list-inside text-gray-700 space-y-2 pl-2">
            <li>Strictly no page refresh/reload allowed</li>
            <li>No switching tabs/windows (2 attempts max)</li>
            <li>No switching tabs/windows (2 attempts max)</li>
            <li>No right-click, copy/paste allowed</li>
            <li>No developer tools access (F12/Ctrl+Shift+I)</li>
            <li>Must remain in fullscreen mode</li>
            <li>Exam will auto-submit when time ends</li>
            <li>Violations may force-submit your exam</li>
          </ul>
        </div>
      </div>
      
      <div class="flex justify-between items-center mt-6 pt-5 border-t border-gray-200">
        <button @click="stage = 'enter'" 
                class="flex items-center bg-gray-100 hover:bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-semibold transition-all duration-200 shadow">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
          </svg>
          Cancel
        </button>
        <button @click="startExam" 
                class="flex items-center bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white px-8 py-3 rounded-lg font-bold shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-0.5">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
          </svg>
          Start Exam Now
        </button>
      </div>
    </div>

    <div v-if="stage === 'exam'" class="w-full max-w-3xl bg-white rounded-2xl shadow-2xl border border-indigo-100 p-10 flex flex-col gap-6 mt-6 z-10">
      <div>
        <div class="text-2xl font-bold text-black mb-6 drop-shadow-sm">
          <span v-if="currentQuestion.Question_Type === 'Fill'" v-html="formatFillQuestion(currentQuestion.Question_Text)"></span>
          <span v-else>{{ currentQuestion.Question_Text }}</span>
        </div>

        <div v-if="currentQuestion.Question_Type === 'MCQ'" class="space-y-5">
          <label v-for="(opt, key) in options" :key="key"
            class="flex items-center space-x-4 p-5 border-2 rounded-lg cursor-pointer transition-all duration-200 shadow-sm"
            :class="{
              'bg-blue-50 border-blue-400 shadow-md scale-105': selectedOption === key,
              'bg-yellow-50 border-yellow-400 shadow-md': keyboardSelectedOption === key && selectedOption !== key,
              'border-gray-200 hover:bg-blue-50 hover:border-blue-300': selectedOption !== key && keyboardSelectedOption !== key
            }"
            @click="selectOption(key)">
            <input type="radio" :value="key" v-model="selectedOption" class="w-5 h-5 text-indigo-600 focus:ring-indigo-500 accent-indigo-600" />
           <span class="text-lg text-black"><span class="font-bold text-black mr-2">{{ key }}.</span>{{ opt }}</span>
          </label>
        </div>

        <div v-else-if="currentQuestion.Question_Type === 'TF'" class="space-y-5">
          <label v-for="(opt, key) in options" :key="key"
            class="flex items-center space-x-4 p-5 border-2 rounded-lg cursor-pointer transition-all duration-200 shadow-sm"
            :class="{
              'bg-blue-50 border-blue-400 shadow-md scale-105': selectedOption === key,
              'bg-yellow-50 border-yellow-400 shadow-md': keyboardSelectedOption === key && selectedOption !== key,
              'border-gray-200 hover:bg-blue-50 hover:border-blue-300': selectedOption !== key && keyboardSelectedOption !== key
            }"
            @click="selectOption(key)">
            <input type="radio" :value="key" v-model="selectedOption" class="w-5 h-5 text-indigo-600 focus:ring-indigo-500 accent-indigo-600" />
           <span class="text-lg text-black"><span class="font-bold text-black mr-2">{{ key }}.</span>{{ opt }}</span>
          </label>
        </div>

        <div v-else-if="currentQuestion.Question_Type === 'Fill'" class="space-y-5">
          <div class="p-5 border-2 border-indigo-200 rounded-lg">
            <label class="block text-lg font-semibold text-gray-700 mb-3">Your Answer:</label>
            <input 
              ref="fillInput"
              v-model="textAnswer" 
              type="text"
              class="w-full p-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-300 focus:border-indigo-400 text-lg"
              placeholder="Type your answer here..."
              @input="clearInlineMessage"
              @keydown.enter="handleNext"
            />
          </div>
        </div>

        <div v-else-if="currentQuestion.Question_Type === 'OneWord'" class="space-y-5">
          <div class="p-5 border-2 border-indigo-200 rounded-lg">
            <label class="block text-lg font-semibold text-gray-700 mb-3">Your Answer:</label>
            <input 
              ref="oneWordInput"
              v-model="textAnswer" 
              type="text"
              class="w-full p-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-300 focus:border-indigo-400 text-lg"
              placeholder="Type your answer here..."
              @input="clearInlineMessage"
              @keydown.enter="handleNext"
            />
          </div>
        </div>

        <div class="flex justify-between items-start mt-10">
          <div class="flex items-start">
            <button 
              v-if="allAnswersFilled"
              @click="finishExam('✅ All questions submitted!')"
              class="bg-gradient-to-r from-purple-600 to-pink-500 hover:from-purple-700 hover:to-pink-600 text-white px-8 py-3 rounded-lg font-bold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 text-lg tracking-wide transition-all duration-300">
              Submit Exam
            </button>
          </div>
          
          <div class="flex-1 mx-4">
            <div v-if="inlineMessage && inlineMessage.type === 'error'" 
                 class="p-3 bg-red-50 border border-red-200 rounded-lg">
              <p class="text-red-700 text-lg font-bold">{{ inlineMessage.text }}</p>
            </div>
            <div v-else-if="inlineMessage && inlineMessage.type === 'success'" 
                 class="p-3 bg-green-50 border border-green-200 rounded-lg">
              <p class="text-green-700 text-lg font-bold">{{ inlineMessage.text }}</p>
            </div>
            <div v-else-if="inlineMessage && inlineMessage.type === 'warning'" 
     class="p-4 rounded-xl border-l-8 border-red-600 bg-red-100 shadow-md">
  <p class="text-red-800 font-semibold text-base tracking-wide">
    {{ inlineMessage.text }}
  </p>
</div>

          </div>
          
          <div class="flex items-start">
            <button @click="handleNext"
              class="bg-gradient-to-r from-indigo-500 via-pink-500 to-rose-500 text-white px-8 py-3 rounded-lg hover:from-indigo-600 hover:to-rose-600 transition-all duration-200 font-bold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 text-lg tracking-wide">
              {{ currentIndex + 1 === questions.length ? 'Submit Exam' : 'Next Question' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <div 
      v-if="stage === 'finished'" 
      :class="[
        'p-10 rounded-2xl shadow-2xl text-center mt-12 z-10 transition-all duration-300',
        finishMessage.includes('forcibly ended') 
          ? 'max-w-2xl bg-red-50 border border-red-300' 
          : 'max-w-md bg-white border border-green-100'
      ]"
    >
      <div class="mb-6">
        <div 
          :class="[
            'w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 shadow text-3xl',
            finishMessage.includes('forcibly ended') 
              ? 'bg-red-100 text-red-600' 
              : 'bg-green-100 text-green-600'
          ]"
        >
          {{ finishMessage.includes('forcibly ended') ? '❌' : '✔️' }}
        </div>

        <h2 
          class="text-2xl font-bold mb-4 whitespace-pre-line text-black"
        >
          {{ finishMessage }}
        </h2>

        <p class="text-lg font-semibold text-black mt-2" v-if="finishMessage.includes('forcibly ended')">
          📩 Please talk to the respective faculty for clarification.
        </p>

        <p class="text-gray-700 mt-3">Your attempt has been recorded.</p>
      </div>

      <div class="bg-gray-50 p-4 rounded-lg shadow">
        <p class="text-sm text-black mb-1">Attempt ID:</p>
        <p class="text-lg font-bold text-black">{{ attemptId }}</p>
      </div>
    </div>
    <div 
  v-if="stage === 'finished'" 
  class="fixed bottom-6 left-6 z-50 bg-yellow-100 border-2 border-yellow-400 text-yellow-900 px-6 py-4 rounded-xl shadow-2xl text-lg font-bold tracking-wide animate-blink"
>
  ⏳ Redirecting to login page in {{ redirectCountdown }} second<span v-if="redirectCountdown !== 1">s</span>...
</div>



  </div>
</template>

<script>
import axios from 'axios'

export default {
 data() {
  return {
    examId: '',
    exam: null,
    questions: [],
    currentIndex: 0,
    selectedOption: null,
    keyboardSelectedOption: null,
    textAnswer: '',
    timer: 0,
    stage: 'enter',
    finishMessage: '',
    attemptId: null,
    examAttemptId: null,
    answers: [],
    optionKeys: ['A', 'B', 'C', 'D'],
    studentEmail: '',
    studentName: '',
    applicantId: null,
    interval: null,
    examIdError: false,
    inlineMessage: null,
    violationCount: 0,
    maxViolations: 3,
    fullscreenRecoveryTimeout: null,
    redirectCountdown: 10,
    redirectTimer: null,
  }
},
  computed: {
  // Get current question
  currentQuestion() {
    return this.questions[this.currentIndex]
  },

  // Return answer options based on question type
  options() {
    const type = this.currentQuestion.Question_Type
    if (type === 'TF') {
      return {
        A: this.currentQuestion.Option_A,
        B: this.currentQuestion.Option_B
      }
    } else if (type === 'MCQ') {
      return {
        A: this.currentQuestion.Option_A,
        B: this.currentQuestion.Option_B,
        C: this.currentQuestion.Option_C,
        D: this.currentQuestion.Option_D
      }
    } else {
      return {}
    }
  },

  // Return option keys like A, B, C, D
  optionKeys() {
    return Object.keys(this.options)
  },

  // Timer minutes
  minutes() {
    return String(Math.floor(this.timer / 60)).padStart(2, '0')
  },

  // Timer seconds
  seconds() {
    return String(this.timer % 60).padStart(2, '0')
  },

  // Check if all questions are answered
  allAnswersFilled() {
    return this.answers.every(ans => ans !== null)
  }
},

  watch: {
    textAnswer() {
      if (this.currentQuestion.Question_Type === 'Fill') {
        this.$forceUpdate()
      }
    }
  },
  
  mounted() {
    this.studentEmail = localStorage.getItem('student_email')
    this.studentName = localStorage.getItem('student_name')
    this.applicantId = parseInt(localStorage.getItem('applicant_id'))

    // Add all event listeners
    window.addEventListener('keydown', this.handleKeydown)
    window.addEventListener('blur', this.handleBlur)
    window.addEventListener('resize', this.detectSplitScreen)
    document.addEventListener('visibilitychange', this.handleVisibilityChange)
    document.addEventListener('fullscreenchange', this.handleFullscreenChange)
    window.addEventListener('beforeunload', this.preventRefresh)
    window.addEventListener('popstate', this.preventBack)
    document.addEventListener('contextmenu', e => e.preventDefault())
    document.addEventListener('cut', e => e.preventDefault())
    document.addEventListener('copy', e => e.preventDefault())
    document.addEventListener('paste', e => e.preventDefault())
    window.history.pushState(null, null, location.href)
  },

  beforeUnmount() {
    clearInterval(this.interval)
    clearTimeout(this.fullscreenRecoveryTimeout)
    clearInterval(this.redirectTimer)
    
    // Remove all event listeners
    window.removeEventListener('keydown', this.handleKeydown)
    window.removeEventListener('blur', this.handleBlur)
    window.removeEventListener('resize', this.detectSplitScreen)
    document.removeEventListener('visibilitychange', this.handleVisibilityChange)
    document.removeEventListener('fullscreenchange', this.handleFullscreenChange)
    window.removeEventListener('beforeunload', this.preventRefresh)
    window.removeEventListener('popstate', this.preventBack)
    document.removeEventListener('contextmenu', e => e.preventDefault())
    document.removeEventListener('cut', e => e.preventDefault())
    document.removeEventListener('copy', e => e.preventDefault())
    document.removeEventListener('paste', e => e.preventDefault())
  },

 methods: {
  formatFillQuestion(text) {
    const value = this.textAnswer || '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
    const safe = value.replace(/</g, '&lt;').replace(/>/g, '&gt;')
    return text.replace(/____+/g, `
      <span class="inline-block border-b-2 border-blue-600 min-w-[120px] px-1 text-center align-baseline text-indigo-800 font-medium tracking-wide">
        ${safe}
      </span>
    `)
  },

  enterFullscreen() {
    const el = document.documentElement
    setTimeout(() => {
      if (el.requestFullscreen) el.requestFullscreen()
      else if (el.webkitRequestFullscreen) el.webkitRequestFullscreen()
      else if (el.mozRequestFullScreen) el.mozRequestFullScreen()
      else if (el.msRequestFullscreen) el.msRequestFullscreen()
    }, 100)
  },

  startRedirectCountdown() {
    this.redirectCountdown = 10;
    this.redirectTimer = setInterval(() => {
      if (this.redirectCountdown > 0) {
        this.redirectCountdown--;
      } else {
        clearInterval(this.redirectTimer);
        localStorage.removeItem('student_email');
        localStorage.removeItem('student_name');
        localStorage.removeItem('applicant_id');
        window.location.href = '/';
      }
    }, 1000);
  },

  // ✅ VIOLATION COUNTED - Alt+Tab (window blur)
  handleBlur() {
    if (this.stage === 'exam') {
      console.log('🚨 Window blur detected (Alt+Tab) - COUNTING VIOLATION')
      this.handleViolation('Window lost focus (Alt+Tab detected)')
      this.recoverFullscreen(100)
    }
  },

  // ✅ VIOLATION COUNTED - Tab switch
  handleVisibilityChange() {
    if (document.hidden && this.stage === 'exam') {
      console.log('🚨 Tab switch detected - COUNTING VIOLATION')
      this.handleViolation('Tab switch detected')
      this.recoverFullscreen(100)
    }
  },

  // ❌ NO VIOLATION - Split screen/window resize (just recover)
  detectSplitScreen() {
    if (this.stage !== 'exam') return
    
    const isFullscreen = document.fullscreenElement !== null
    const screenWidth = window.screen.width
    const screenHeight = window.screen.height
    const windowWidth = window.innerWidth
    const windowHeight = window.innerHeight
    
    if (!isFullscreen) {
      console.log('⚠️ Not in fullscreen - recovering (no violation)')
      this.recoverFullscreen(100)
      return
    }
    
    const widthRatio = windowWidth / screenWidth
    const heightRatio = windowHeight / screenHeight
    
    if (widthRatio < 0.95 || heightRatio < 0.95) {
      console.log('⚠️ Window resize detected - recovering (no violation)')
      this.recoverFullscreen(100)
    }
  },

  // ❌ NO VIOLATION - Fullscreen exit (system action)
  handleFullscreenChange() {
    if (this.stage === 'exam' && !document.fullscreenElement) {
      console.log('⚠️ Fullscreen exited - recovering (no violation)')
      this.recoverFullscreen(100)
    }
  },

  handleViolation(reason) {
    this.violationCount++
    console.log(`⚠️ VIOLATION #${this.violationCount}: ${reason}`)
    
    if (this.violationCount >= this.maxViolations) {
      this.forceExit(reason)
    } else {
      const left = this.maxViolations - this.violationCount
      this.showInlineMessage(`⚠️ Warning ${this.violationCount}/${this.maxViolations}: ${reason}. You have ${left} attempt(s) left.`, 'warning')
    }
  },
  	
  async forceExit(reason) {
    clearInterval(this.interval)
    
    // 1. Prepare answers for submission 
    this.answers = this.answers.map((ans, idx) => {
      if (ans === null) {
        return {
          question_id: this.questions[idx].Question_Id,
          selected_option: '' // Submit empty string for unanswered
        }
      }
      return ans
    })
    
    // 2. Call the Submission API with restriction flag (Uses corrected keys)
    try {
        const submissionRes = await axios.post('http://localhost:5000/api/student/submit', {
            applicant_id: this.applicantId,
            exam_paper_id: this.exam.Exam_Paper_Id,
            answers: this.answers,
            attempt_id: this.examAttemptId,
            is_restricted: true, 
            restriction_reason: reason 
        })
        this.attemptId = submissionRes.data.Attempt_Id
        console.log("Forced submission successful, attempt ID:", this.attemptId)
    } catch (error) {
        console.error("Forced submission error:", error)
        this.attemptId = this.examAttemptId || 'N/A' 
    }
  	
    // 3. Update UI and Logout
    this.stage = 'finished'
    this.finishMessage = `Exam forcibly ended.\nReason: ${reason}\n\nTotal Violations: ${this.violationCount}/${this.maxViolations}`

    window.removeEventListener('beforeunload', this.preventRefresh)
    
    this.startRedirectCountdown()
  },
  	
  recoverFullscreen(delay = 100) {
    clearTimeout(this.fullscreenRecoveryTimeout)
    this.fullscreenRecoveryTimeout = setTimeout(() => {
      if (this.stage === 'exam' && !document.fullscreenElement) {
        console.log("🔄 Re-entering fullscreen after", delay, "ms delay")
        this.enterFullscreen()
      }
    }, delay)
  },

  preventRefresh(e) {
    e.preventDefault()
    e.returnValue = ''
  },

  preventBack() {
    window.history.pushState(null, null, location.href)
  },

  handleKeydown(event) {
    if (this.stage !== 'exam') return;

    const qType = this.currentQuestion.Question_Type;
    if (['MCQ', 'TF'].includes(qType)) {
      const key = event.key;
      if (['ArrowUp', 'ArrowDown'].includes(key)) {
        event.preventDefault();
        this.navigateOptions(key === 'ArrowUp' ? -1 : 1);
      } else if (key === 'Enter') {
        event.preventDefault();
        this.handleEnterKey();
      }
    }

    // ✅ VIOLATION COUNTED - ESC key
    if (event.key === 'Escape') {
      event.preventDefault();
      event.stopPropagation();
      
      console.log('🚨 ESC key pressed - COUNTING VIOLATION');
      this.violationCount++;
  	
      // Check if reached max
      if (this.violationCount >= this.maxViolations) {
        this.forceExit('ESC key pressed (attempted to exit fullscreen)');
  	  return;
      }
  	
      // Show warning
      const left = this.maxViolations - this.violationCount;
      this.showInlineMessage(
        `⚠️ Warning ${this.violationCount}/${this.maxViolations}: ESC key pressed. You have ${left} attempt(s) left.`, 
        'warning'
      );
  	
      // Immediately re-enter fullscreen 
      setTimeout(() => this.enterFullscreen(), 100);
  	  return;
    }

    // ❌ NO VIOLATION - Browser-locked keys (F12, DevTools, Ctrl+R, Ctrl+U)
    const isRestrictedCombo =
      event.key === 'F12' ||
      (event.ctrlKey && event.shiftKey && ['I', 'C', 'J'].includes(event.key.toUpperCase())) ||
      (event.ctrlKey && (event.key.toUpperCase() === 'U' || event.key.toUpperCase() === 'R')) || 
      (event.ctrlKey && event.key === 'Tab');

    if (isRestrictedCombo) {
      event.preventDefault();
      console.log('🔒 Restricted key blocked (no violation - browser locked):', event.key);
      return;
    }

    // ❌ NO VIOLATION - Screenshot keys
    if (event.key === 'PrintScreen' || 
        (event.metaKey && event.shiftKey && ['3', '4', '5'].includes(event.key))) {
      event.preventDefault();
      console.log('🔒 Screenshot blocked (no violation)');
      return;
    }
  },

  navigateOptions(dir) {
    const availableKeys = Object.keys(this.options)
    const index = this.keyboardSelectedOption
      ? availableKeys.indexOf(this.keyboardSelectedOption)
      : (this.selectedOption ? availableKeys.indexOf(this.selectedOption) : -1)
    let newIndex = index + dir
    if (newIndex < 0) newIndex = availableKeys.length - 1
    if (newIndex >= availableKeys.length) newIndex = 0
    this.keyboardSelectedOption = availableKeys[newIndex]
  },

  handleEnterKey() {
    if (this.keyboardSelectedOption) {
      this.selectOption(this.keyboardSelectedOption)
      this.keyboardSelectedOption = null
    } else if (this.selectedOption || this.textAnswer) {
      this.handleNext()
    } else {
      this.showInlineMessage('⚠️ Select or enter an answer first', 'warning')
    }
  },

  selectOption(key) {
    this.selectedOption = key
    this.keyboardSelectedOption = null
    this.clearInlineMessage()
  },

  async fetchExam() {
    try {
      this.examIdError = false
      this.clearInlineMessage()
  	
  	  // Must use POST for security when sending applicant_id
  	  const res = await axios.post(`http://localhost:5000/api/student/exam/${this.examId}`, {
        applicant_id: this.applicantId
  	  })
  	
  	  this.exam = res.data.exam
  	  this.questions = res.data.questions
  	  this.answers = new Array(this.questions.length).fill(null)
  	
  	  // Use the attempt_id returned by the endpoint (if any existing attempt is In Progress)
  	  this.examAttemptId = res.data.attempt_id 
  	  
  	  // Set timer based on remaining time if continuing an attempt, otherwise full duration
  	  if (res.data.exam.Remaining_Seconds !== undefined && res.data.attempt_id) {
          this.timer = res.data.exam.Remaining_Seconds
  	  } else {
  	      this.timer = this.exam.Duration_Minutes * 60
  	  }
  	
  	  this.stage = 'instructions'
  	  this.clearInlineMessage()
  	
  	} catch (error) {
  	  this.examIdError = true
  	  console.error("Fetch exam error:", error)
  	  
  	  if (error.response) {
  	    const status = error.response.status
  	    const errorData = error.response.data
  	    
  	    switch (status) {
  	      case 425:
  	      case 410:
  	      case 403:
  	      case 409:
  	      case 404:
  	        this.showInlineMessage(errorData.error || errorData.message || 'Error accessing exam.', 'error')
  	        break
  	      default:
  	        this.showInlineMessage(errorData.error || 'Failed to load exam. Please try again.', 'error')
  	    }
  	  } else {
  	    this.showInlineMessage('Network error. Please check your connection.', 'error')
  	  }
  	}
  },

  startExam() {
    // 1. Start Exam Attempt on Backend (Get/Confirm Attempt ID)
    axios.post('http://localhost:5000/api/student/start-exam', {
        applicant_id: this.applicantId,
        exam_id: this.exam.Exam_Id
    })
    .then(response => {
        // This is only executed if the backend confirms the start (new attempt created or existing 'In Progress' returned)
        if (response.data.attempt_id) {
            this.examAttemptId = response.data.attempt_id;
            console.log("Attempt started on backend. ID:", this.examAttemptId);
        }

        // 2. Start Frontend UI and Timer
        this.stage = 'exam'
        this.enterFullscreen()
        
        console.log("🚀 Starting exam with timer:", this.timer, "seconds")
        
        this.interval = setInterval(() => {
          if (this.timer > 0) {
            this.timer--
            
            if (this.timer === 300) {
              this.showInlineMessage('⚠️ Only 5 minutes remaining!', 'warning')
            } else if (this.timer === 60) {
              this.showInlineMessage('🚨 Only 1 minute remaining!', 'warning')
            }
            
          } else {
            clearInterval(this.interval)
            this.handleTimerFinish()
          }
        }, 1000)

        // 3. Initial checks
        this.loadCurrentAnswer()
        setTimeout(() => {
          if (this.stage === 'exam' && !document.fullscreenElement) {
            this.enterFullscreen()
          }
        }, 1000)

    })
    .catch(error => {
        console.error("Failed to start attempt on backend:", error);
        this.showInlineMessage(
            error.response?.data?.message || error.response?.data?.error || 'Failed to start exam. Server error.',
            'error'
        );
        this.stage = 'enter'; // Go back to enter stage on failure
    });
},

  handleTimerFinish() {
    console.log("⏰ Timer finished - auto submitting exam")
    
    // Prepare all questions, including unanswered ones with empty string
    this.answers = this.answers.map((ans, idx) => {
      if (ans === null) {
        return {
          question_id: this.questions[idx].Question_Id,
          selected_option: '' // Submit empty string for unanswered
        }
      }
      return ans
    })

    this.finishExam('⏰ Time is up!\nYour exam has been auto-submitted.')
  },

  handleNext() {
    const type = this.currentQuestion.Question_Type
    let value = null

    if (type === 'MCQ' || type === 'TF') {
      if (!this.selectedOption) {
        this.showInlineMessage('⚠️ Select an option first', 'warning')
        return
      }
      value = this.selectedOption
    } else if (type === 'Fill' || type === 'OneWord') {
      if (!this.textAnswer.trim()) {
        this.showInlineMessage('⚠️ Please provide an answer', 'warning')
        return
      }
      value = this.textAnswer.trim()
    }

    this.answers[this.currentIndex] = {
      question_id: this.currentQuestion.Question_Id,
      selected_option: value
    }

    const last = this.currentIndex + 1 === this.questions.length

    if (last) {
      const anyUnanswered = this.answers.some(ans => ans === null)
      if (anyUnanswered) {
        this.showInlineMessage('⚠️ Please answer all questions.', 'warning')
        return
      }

      clearInterval(this.interval)
      this.finishExam('✅ All questions submitted!')
    } else {
      this.selectedOption = null
      this.textAnswer = ''
      this.keyboardSelectedOption = null
      this.clearInlineMessage()

      this.currentIndex++
      this.loadCurrentAnswer()
      this.focusTextInput()
    }
  },

  loadCurrentAnswer() {
    const ans = this.answers[this.currentIndex]
    const type = this.currentQuestion.Question_Type
    if (ans) {
      if (type === 'MCQ' || type === 'TF') this.selectedOption = ans.selected_option
      else this.textAnswer = ans.selected_option
    } else {
      this.selectedOption = null
      this.textAnswer = ''
    }
    this.keyboardSelectedOption = null
    this.clearInlineMessage()
    this.$nextTick(() => {
      if (this.currentQuestion.Question_Type === 'Fill' && this.$refs.fillInput) {
        this.$refs.fillInput.focus()
      } else if (this.currentQuestion.Question_Type === 'OneWord' && this.$refs.oneWordInput) {
        this.$refs.oneWordInput.focus()
      }
    })
  },

  jumpToQuestion(idx) {
    this.currentIndex = idx
    this.loadCurrentAnswer()
  },
  	
  async finishExam(msg) {
    this.stage = 'finished'
    this.finishMessage = msg

    // Prevent accidental navigation after submission
    window.removeEventListener('beforeunload', this.preventRefresh)

    try {
  	  // 1. Submit answers (backend handles grading & logging out)
  	  const submissionRes = await axios.post('http://localhost:5000/api/student/submit', {
        applicant_id: this.applicantId,
        exam_paper_id: this.exam.Exam_Paper_Id,
        answers: this.answers,
        attempt_id: this.examAttemptId,
        is_restricted: false, 
        restriction_reason: null 
  	  })
  	  this.attemptId = submissionRes.data.Attempt_Id
  	  console.log("Submission successful, attempt ID:", this.attemptId)
  	} catch (error) {
  	  console.error("Submission error:", error)
  	  this.showInlineMessage('Submission failed', 'error')
  	  this.attemptId = this.examAttemptId || 'N/A'
  	}

    // 2. Start redirect countdown
    this.startRedirectCountdown()
  },

  showInlineMessage(text, type = 'error') {
    this.inlineMessage = { text, type }
    setTimeout(() => {
      this.clearInlineMessage()
    }, 5000)
  },

  clearInlineMessage() {
    this.inlineMessage = null
  },

  focusTextInput() {
    this.$nextTick(() => {
      if (this.currentQuestion.Question_Type === 'Fill' && this.$refs.fillInput) {
        this.$refs.fillInput.focus()
      } else if (this.currentQuestion.Question_Type === 'OneWord' && this.$refs.oneWordInput) {
        this.$refs.oneWordInput.focus()
      }
    })
  }
 }
}
</script>
<style>
@keyframes blink {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.05); }
}

.animate-blink {
  animation: blink 1.2s infinite;
}

</style>