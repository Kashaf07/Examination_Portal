<template>
  <!-- Student Info Box - Fixed Position -->
  <div class="fixed top-4 right-6 z-50 group">
    <div class="bg-white px-6 py-3 rounded-2xl shadow-lg border-2 border-black text-base font-semibold text-indigo-800 cursor-default transition-all duration-300 hover:shadow-xl hover:scale-105">
      👤 {{ studentName || studentEmail }}
    </div>
    
    <!-- Email Tooltip -->
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

  <div class="min-h-screen w-full flex flex-col relative bg-gradient-to-br from-[#d2eaf6] via-[#e1f5fe] to-[#e0f7fa] overflow-hidden">
    <!-- Decorative SVG Waves - Always at bottom -->
    <svg class="absolute bottom-0 left-0 w-full h-48 md:h-64 lg:h-72 z-0" viewBox="0 0 1440 320" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path fill="#b3e0f2" d="M0,224L60,202.7C120,181,240,139,360,144C480,149,600,203,720,197.3C840,192,960,128,1080,117.3C1200,107,1320,149,1380,170.7L1440,192V320H0Z"/>
      <path fill="#cbe7f7" fill-opacity="0.7" d="M0,288L60,272C120,256,240,224,360,197.3C480,171,600,149,720,154.7C840,160,960,192,1080,197.3C1200,203,1320,181,1380,170.7L1440,160V320H0Z"/>
      <path fill="#e0f7fa" fill-opacity="0.5" d="M0,320L60,293.3C120,267,240,213,360,197.3C480,181,600,203,720,197.3C840,192,960,160,1080,154.7C1200,149,1320,171,1380,181.3L1440,192V320H0Z"/>
    </svg>

    <!-- Content Container - Above waves -->
    <div class="flex-1 w-full flex items-center justify-center z-10 py-6">
      <!-- Exam ID Entry Stage -->
      <ExamIdEntry 
        v-if="stage === 'enter'"
        :inline-message="inlineMessage"
        :exam-id-error="examIdError"
        @fetch-exam="fetchExam"
      />

      <!-- Instructions Stage -->
      <ExamInstructions
        v-if="stage === 'instructions'"
        :exam="exam"
        :questions-count="questions.length"
        @go-back="goBackToEntry"
        @start-exam="startExam"
      />

      <!-- Exam Stage -->
      <ExamInterface
        v-if="stage === 'exam'"
        :timer="timer"
        :questions="questions"
        :current-index="currentIndex"
        :current-question="currentQuestion"
        :selected-option="selectedOption"
        :keyboard-selected-option="keyboardSelectedOption"
        :text-answer="textAnswer"
        v-model:text-answer="textAnswer"
        :answers="answers"
        :violation-count="violationCount"
        :inline-message="inlineMessage"
        :visited-questions="visitedQuestions"
        @jump-to-question="jumpToQuestion"
        @select-option="selectOption"
        @finish-exam="finishExam"
        @handle-next="handleNext"
      />

      <!-- Finished Stage -->
      <ExamFinished
        v-if="stage === 'finished'"
        :finish-message="finishMessage"
        :attempt-id="attemptId"
        :redirect-countdown="redirectCountdown"
      />
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import ExamIdEntry from '../components/ExamIdEntry.vue'
import ExamInstructions from '../components/ExamInstructions.vue'
import ExamInterface from '../components/ExamInterface.vue'
import ExamFinished from '../components/ExamFinished.vue'

export default {
  components: {
    ExamIdEntry,
    ExamInstructions,
    ExamInterface,
    ExamFinished
  },

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
      isProcessingViolation: false,
      visitedQuestions: []
    }
  },

  computed: {
    currentQuestion() {
      return this.questions[this.currentIndex]
    }
  },

  mounted() {
    this.studentEmail = localStorage.getItem('student_email')
    this.studentName = localStorage.getItem('student_name')
    this.applicantId = parseInt(localStorage.getItem('applicant_id'))

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

    window.removeEventListener('keydown', this.handleKeydown)
    window.removeEventListener('blur', this.handleBlur)
    window.removeEventListener('resize', this.detectSplitScreen)
    document.removeEventListener('visibilitychange', this.handleVisibilityChange)
    document.removeEventListener('fullscreenchange', this.handleFullscreenChange)
    window.removeEventListener('beforeunload', this.preventRefresh)
    window.removeEventListener('popstate', this.preventBack)
  },

  methods: {
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
      this.redirectCountdown = 10
      this.redirectTimer = setInterval(() => {
        if (this.redirectCountdown > 0) {
          this.redirectCountdown--
        } else {
          clearInterval(this.redirectTimer)
          localStorage.removeItem('student_email')
          localStorage.removeItem('student_name')
          localStorage.removeItem('applicant_id')
          window.location.href = '/'
        }
      }, 1000)
    },

    handleBlur() {
      if (this.stage === 'exam' && !this.isProcessingViolation) {
        this.isProcessingViolation = true
        this.handleViolation('Window lost focus (Alt+Tab detected)')
        setTimeout(() => {
          this.recoverFullscreen(100)
          this.isProcessingViolation = false
        }, 500)
      }
    },

    handleVisibilityChange() {
      if (document.hidden && this.stage === 'exam' && !this.isProcessingViolation) {
        this.isProcessingViolation = true
        this.handleViolation('Tab switch detected')
        setTimeout(() => {
          this.recoverFullscreen(100)
          this.isProcessingViolation = false
        }, 500)
      }
    },

    detectSplitScreen() {
      if (this.stage !== 'exam' || this.isProcessingViolation) return
      const isFullscreen = document.fullscreenElement !== null
      const screenWidth = window.screen.width
      const screenHeight = window.screen.height
      const windowWidth = window.innerWidth
      const windowHeight = window.innerHeight
      if (!isFullscreen) {
        this.recoverFullscreen(100)
        return
      }
      const widthRatio = windowWidth / screenWidth
      const heightRatio = windowHeight / screenHeight
      if (widthRatio < 0.95 || heightRatio < 0.95) {
        this.recoverFullscreen(100)
      }
    },

    handleFullscreenChange() {
      if (this.stage === 'exam' && !document.fullscreenElement && !this.isProcessingViolation) {
        this.isProcessingViolation = true
        setTimeout(() => {
          this.recoverFullscreen(100)
          this.isProcessingViolation = false
        }, 300)
      }
    },

    handleViolation(reason) {
      this.violationCount++
      if (this.violationCount >= this.maxViolations) {
        this.forceExit(reason)
      } else {
        const left = this.maxViolations - this.violationCount
        this.showInlineMessage(
          `⚠️ Warning ${this.violationCount}/${this.maxViolations}: ${reason}. You have ${left} attempt(s) left.`,
          'warning'
        )
      }
    },

    async forceExit(reason) {
      clearInterval(this.interval)
      this.stage = 'finished'
      this.finishMessage = `Exam forcibly ended.\nReason: ${reason}\n\nTotal Violations: ${this.violationCount}/${this.maxViolations}`
      window.removeEventListener('beforeunload', this.preventRefresh)
      
      try {
        if (this.examAttemptId) {
          const res = await axios.post('http://localhost:5000/api/student/report-restriction', {
            attempt_id: this.examAttemptId,
            applicant_id: this.applicantId,
            exam_paper_id: this.exam.Exam_Paper_Id,
            reason: reason || 'Misconduct'
          })
          if (res.data && res.data.attempt_id) {
            this.attemptId = res.data.attempt_id
          } else {
            this.attemptId = this.examAttemptId
          }
        } else {
          this.attemptId = 'N/A'
        }
      } catch (error) {
        console.error('Forced end API failed:', error)
        this.attemptId = this.examAttemptId || 'N/A'
      }

      const email = localStorage.getItem('student_email')
      if (email) {
        try {
          await axios.post('http://localhost:5000/api/logout', { email: email, role: 'Student' })
        } catch {}
      }
      this.startRedirectCountdown()
    },

    recoverFullscreen(delay = 100) {
      clearTimeout(this.fullscreenRecoveryTimeout)
      this.fullscreenRecoveryTimeout = setTimeout(() => {
        if (this.stage === 'exam' && !document.fullscreenElement) {
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
      if (this.stage !== 'exam') return

      const qType = this.currentQuestion.Question_Type
      if (['MCQ', 'TF'].includes(qType)) {
        const key = event.key
        if (['ArrowUp', 'ArrowDown'].includes(key)) {
          event.preventDefault()
          this.navigateOptions(key === 'ArrowUp' ? -1 : 1)
        } else if (key === 'Enter') {
          event.preventDefault()
          this.handleEnterKey()
        }
      }

      if (event.key === 'Escape') {
        event.preventDefault()
        event.stopPropagation()
        this.violationCount++
        
        if (this.violationCount >= this.maxViolations) {
          this.forceExit('ESC key pressed (attempted to exit fullscreen)')
          return
        }
        
        const left = this.maxViolations - this.violationCount
        this.showInlineMessage(
          `⚠️ Warning ${this.violationCount}/${this.maxViolations}: ESC key pressed. You have ${left} attempt(s) left.`, 
          'warning'
        )
        
        setTimeout(() => this.enterFullscreen(), 100)
        return
      }

      const isRestrictedCombo =
        event.key === 'F12' ||
        (event.ctrlKey && event.shiftKey && ['I', 'C', 'J'].includes(event.key)) ||
        (event.ctrlKey && ['U'].includes(event.key)) ||
        (event.ctrlKey && event.key === 'Tab')

      if (isRestrictedCombo) {
        event.preventDefault()
        return
      }

      const isRefreshKey =
        event.key === 'F5' ||
        (event.ctrlKey && event.key === 'r') ||
        (event.ctrlKey && event.key === 'R') ||
        (event.ctrlKey && event.shiftKey && event.key === 'r') ||
        (event.ctrlKey && event.shiftKey && event.key === 'R')

      if (isRefreshKey) {
        event.preventDefault()
        return
      }

      if (event.key === 'PrintScreen' || 
          (event.metaKey && event.shiftKey && ['3', '4', '5'].includes(event.key))) {
        event.preventDefault()
        return
      }
    },

    navigateOptions(dir) {
      const type = this.currentQuestion.Question_Type
      const options = type === 'TF' 
        ? { A: this.currentQuestion.Option_A, B: this.currentQuestion.Option_B }
        : type === 'MCQ'
        ? {
            A: this.currentQuestion.Option_A,
            B: this.currentQuestion.Option_B,
            C: this.currentQuestion.Option_C,
            D: this.currentQuestion.Option_D
          }
        : {}
      
      const availableKeys = Object.keys(options)
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

    goBackToEntry() {
      this.stage = 'enter'
      this.examIdError = false
      this.clearInlineMessage()
      this.exam = null
      this.questions = []
      this.examAttemptId = null
      this.currentIndex = 0
      this.answers = []
      this.visitedQuestions = []
    },

    async fetchExam(examId) {
      this.examId = examId
      try {
        this.examIdError = false
        this.clearInlineMessage()
        
        const res = await axios.post(`http://localhost:5000/api/student/exam/${this.examId}`, {
          applicant_id: this.applicantId
        })
        
        this.exam = res.data.exam
        this.questions = res.data.questions
        this.answers = new Array(this.questions.length).fill(null)
        this.examAttemptId = res.data.attempt_id || null
        
        if (res.data.exam.Remaining_Seconds !== undefined) {
          this.timer = res.data.exam.Remaining_Seconds
        } else {
          this.timer = this.exam.Duration_Minutes * 60
        }
        
        this.stage = 'instructions'
        this.clearInlineMessage()
      } catch (error) {
        this.examIdError = true
        if (error.response) {
          const status = error.response.status
          const errorData = error.response.data
          switch (status) {
            case 425:
              this.showInlineMessage(
                errorData.error || 'Exam has not started yet. Please wait until the scheduled time.',
                'error'
              )
              break
            case 410:
              this.showInlineMessage(
                errorData.error || 'Exam entry time has expired. You cannot start the exam after 10 minutes of exam start time.',
                'error'
              )
              break
            case 403:
              this.showInlineMessage(
                errorData.error || 'Access Denied: You are not assigned to this exam',
                'error'
              )
              break
            case 409:
              this.showInlineMessage(
                errorData.error || 'You have already attempted this exam',
                'error'
              )
              break
            case 404:
              this.showInlineMessage('Invalid Exam ID', 'error')
              break
            default:
              this.showInlineMessage(
                errorData.error || 'Failed to load exam. Please try again.',
                'error'
              )
          }
        } else {
          this.showInlineMessage('Network error. Please check your connection.', 'error')
        }
      }
    },

    async startExam() {
      try {
        const res = await axios.post('http://localhost:5000/api/student/start-exam', {
          applicant_id: this.applicantId,
          exam_id: this.exam.Exam_Id
        })

        if (res.data && res.data.attempt_id) {
          this.examAttemptId = res.data.attempt_id
          console.log('✅ Exam attempt created:', this.examAttemptId)
        }

        this.stage = 'exam'
        this.enterFullscreen()
        
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
        
        setTimeout(() => {
          if (this.stage === 'exam' && !document.fullscreenElement) {
            this.enterFullscreen()
          }
        }, 1000)
      } catch (error) {
        console.error('Failed to start exam attempt:', error)
        this.showInlineMessage('Failed to start exam. Please try again.', 'error')
      }
    },

    handleTimerFinish() {
      this.answers = this.answers.map((ans, idx) => {
        if (ans === null) {
          return {
            question_id: this.questions[idx].Question_Id,
            selected_option: ''
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
          // Mark all unanswered questions as visited/skipped
          this.questions.forEach((_, idx) => {
            if (this.answers[idx] === null && !this.visitedQuestions.includes(idx)) {
              this.visitedQuestions.push(idx)
            }
          })
          
          // Wait a bit to show the yellow color change
          setTimeout(() => {
            this.showInlineMessage('⚠️ Please answer all questions.', 'warning')
          }, 100)
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
    },

    jumpToQuestion(idx) {
      // Mark current question as visited before jumping
      if (!this.visitedQuestions.includes(this.currentIndex)) {
        this.visitedQuestions.push(this.currentIndex)
      }
      
      this.currentIndex = idx
      this.loadCurrentAnswer()
    },

    async finishExam(msg) {
      // Mark all unanswered questions as visited/skipped
      this.questions.forEach((_, idx) => {
        if (this.answers[idx] === null && !this.visitedQuestions.includes(idx)) {
          this.visitedQuestions.push(idx)
        }
      })
      
      this.stage = 'finished'
      this.finishMessage = msg
      window.removeEventListener('beforeunload', this.preventRefresh)
      
      const email = localStorage.getItem('student_email')
      if (email) {
        try {
          await axios.post('http://localhost:5000/api/logout', {
            email: email,
            role: 'Student'
          })
        } catch (error) {
          console.error('Logout API failed:', error)
        }
      }
      
      this.startRedirectCountdown()
      
      try {
        const res = await axios.post('http://localhost:5000/api/student/submit', {
          applicant_id: this.applicantId,
          exam_paper_id: this.exam.Exam_Paper_Id,
          answers: this.answers,
          attempt_id: this.examAttemptId
        })
        this.attemptId = res.data.Attempt_Id || this.examAttemptId || 'N/A'
      } catch (error) {
        console.error('Submission error:', error)
        this.attemptId = this.examAttemptId || 'N/A'
        this.showInlineMessage('Submission failed', 'error')
      }
    },

    showInlineMessage(text, type = 'error') {
      this.inlineMessage = { text, type }
      setTimeout(() => {
        this.clearInlineMessage()
      }, 5000)
    },

    clearInlineMessage() {
      this.inlineMessage = null
    }
  }
}
</script>