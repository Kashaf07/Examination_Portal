<template>
  <!-- Student Info Box + Logout - Fixed Position -->
  <div class="fixed top-4 right-6 z-50 flex flex-col items-end gap-4">
    <!-- Name/Email box -->
    <div class="group relative">
      <div class="bg-white/90 backdrop-blur-sm px-5 py-2.5 rounded-2xl shadow-md border border-indigo-100 text-base font-semibold text-indigo-700 cursor-default transition-all duration-300 hover:shadow-lg">
        👤 {{ studentName || studentEmail }}
      </div>
      <!-- Email Tooltip -->
      <div class="absolute top-full right-0 mt-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 transform translate-y-1 group-hover:translate-y-0 z-50">
        <div class="bg-gradient-to-r from-emerald-500 to-teal-600 text-white px-4 py-3 rounded-xl shadow-2xl min-w-max relative">
          <div class="absolute -top-2 right-4 w-4 h-4 bg-emerald-500 transform rotate-45"></div>
          <div class="relative z-10">
            <div class="text-xs font-medium text-emerald-100 mb-1">📧 Email Address</div>
            <div class="text-sm font-bold text-white tracking-wide">{{ studentEmail }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Logout icon button — only on enter stage -->
    <button
      v-if="stage === 'enter'"
      @click="showLogoutConfirm = true"
      class="bg-white/90 backdrop-blur-sm w-14 h-14 rounded-2xl shadow-lg border border-gray-200 flex items-center justify-center hover:bg-red-50 hover:border-red-200 hover:shadow-xl transition-all duration-200 group/btn"
      title="Logout"
    >
      <svg class="w-6 h-6 text-gray-500 group-hover/btn:text-red-500 transition-colors duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
      </svg>
    </button>
  </div>

  <!-- Logout Confirmation Modal -->
  <div
    v-if="showLogoutConfirm"
    class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/40 backdrop-blur-sm"
  >
    <div class="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-sm mx-4">
      <h3 class="text-lg font-bold text-gray-900 mb-2">Logout</h3>
      <p class="text-sm text-gray-500 mb-7">Are you sure you want to logout?</p>
      <div class="flex gap-3">
        <button
          @click="showLogoutConfirm = false"
          class="flex-1 py-2.5 rounded-xl border border-gray-300 text-gray-600 font-semibold text-sm hover:bg-gray-50 transition"
        >
          Cancel
        </button>
        <button
          @click="confirmLogout"
          class="flex-1 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm transition"
        >
          Logout
        </button>
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
        ref="examInterface"
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
        @show-inline-message="showInlineMessage"
        :outside-countdown="outsideCountdown"
        :is-outside-screen="isOutsideScreen"
        :battery-level="batteryLevel"
        :is-online="isOnline"
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
// ✅ Use axiosInstance for all API calls (consistent base URL + headers)
import axiosInstance from '../utils/axiosInstance'
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
      outsideCountdown: 0,
      outsideTimer: null,
      isOutsideScreen: false,
      violationCount: 0,
      maxViolations: 3,
      fullscreenRecoveryTimeout: null,
      redirectCountdown: 10,
      redirectTimer: null,
      isProcessingViolation: false,
      visitedQuestions: [],

      // ── Key-log queue: batch-send every 3 seconds to reduce HTTP overhead ──
      _keyLogQueue: [],
      _keyLogFlushTimer: null,

      // ── System monitoring: battery and WiFi ──
      batteryLevel: 100,
      isOnline: navigator.onLine,
      batteryMonitor: null,

      showLogoutConfirm: false,
      showLogoutHint: false
    }
  },

  computed: {
    currentQuestion() {
      return this.questions[this.currentIndex]
    }
  },
  watch: {
  textAnswer(newVal) {
    if (this.stage !== 'exam') return

    this.answers[this.currentIndex] = {
      question_id: this.currentQuestion.Question_Id,
      selected_option: newVal
    }

    this.saveAnswersLocal()
  }
},


  mounted() {
    this.studentEmail = localStorage.getItem('student_email') || localStorage.getItem('email') || ''
    this.studentName  = localStorage.getItem('student_name')  || localStorage.getItem('name')  || ''
    this.applicantId  = parseInt(localStorage.getItem('applicant_id'))

    // Show logout hint for 2s on first load
    setTimeout(() => {
      this.showLogoutHint = true
      setTimeout(() => { this.showLogoutHint = false }, 2000)
    }, 800)

    window.addEventListener('keydown',          this.handleKeydown)
    window.addEventListener('focus',            this.cancelOutsideCountdown)
    window.addEventListener('blur',             this.handleBlur)
    window.addEventListener('resize',           this.detectSplitScreen)
    document.addEventListener('visibilitychange', this.handleVisibilityChange)
    document.addEventListener('fullscreenchange', this.handleFullscreenChange)
    window.addEventListener('beforeunload',     this.preventRefresh)
    window.addEventListener('popstate',         this.preventBack)
    document.addEventListener('contextmenu',    e => e.preventDefault())

    // ─── Monitor battery and WiFi status ─────────────────────────────────────
    window.addEventListener('online',  () => { this.isOnline = true })
    window.addEventListener('offline', () => { this.isOnline = false })
    this.startBatteryMonitoring()

    // ─── Copy / Paste / Cut — block + log ────────────────────────────────────
    document.addEventListener('cut',  this._handleCut  = (e) => {
      e.preventDefault()
      this.logKey('Ctrl+X', 'blocked', { ctrlKey: true, shiftKey: false, altKey: false, metaKey: false })
    })
    document.addEventListener('copy', this._handleCopy = (e) => {
      e.preventDefault()
      this.logKey('Ctrl+C', 'blocked', { ctrlKey: true, shiftKey: false, altKey: false, metaKey: false })
    })
    document.addEventListener('paste', this._handlePaste = (e) => {
      e.preventDefault()
      this.logKey('Ctrl+V', 'blocked', { ctrlKey: true, shiftKey: false, altKey: false, metaKey: false })
    })

    window.history.pushState(null, null, location.href)
  },

  beforeUnmount() {
    // Flush any remaining queued key logs before unmounting
    this._flushKeyLogs()

    if (this.autoSaveTimer) {
  clearInterval(this.autoSaveTimer)
}
    clearTimeout(this.fullscreenRecoveryTimeout)
    clearInterval(this.redirectTimer)
    clearInterval(this._keyLogFlushTimer)
    clearInterval(this.batteryMonitor)

    window.removeEventListener('focus',           this.cancelOutsideCountdown)
    window.removeEventListener('keydown',         this.handleKeydown)
    window.removeEventListener('blur',            this.handleBlur)
    window.removeEventListener('resize',          this.detectSplitScreen)
    document.removeEventListener('visibilitychange', this.handleVisibilityChange)
    document.removeEventListener('fullscreenchange', this.handleFullscreenChange)
    window.removeEventListener('beforeunload',    this.preventRefresh)
    window.removeEventListener('popstate',        this.preventBack)
    document.removeEventListener('cut',           this._handleCut)
    document.removeEventListener('copy',          this._handleCopy)
    document.removeEventListener('paste',         this._handlePaste)
  },

  methods: {

    confirmLogout() {
      this.showLogoutConfirm = false
      localStorage.clear()
      this.$router.push('/')
    },

    startRedirectCountdown() {
      this.redirectCountdown = 10
      this.redirectTimer = setInterval(() => {
        this.redirectCountdown--
        if (this.redirectCountdown <= 0) {
          clearInterval(this.redirectTimer)
          localStorage.clear()
          this.$router.push('/')
        }
      }, 1000)
    },

    // ─── Battery Monitoring ───────────────────────────────────────────────────
    async startBatteryMonitoring() {
      try {
        if ('getBattery' in navigator) {
          const battery = await navigator.getBattery()
          this.batteryLevel = Math.round(battery.level * 100)

          battery.addEventListener('levelchange', () => {
            this.batteryLevel = Math.round(battery.level * 100)
          })

          // Update battery every 30 seconds
          this.batteryMonitor = setInterval(async () => {
            const bat = await navigator.getBattery()
            this.batteryLevel = Math.round(bat.level * 100)
          }, 30000)
        }
      } catch (err) {
        console.warn('Battery API not supported')
      }
    },

    // ─── Keystroke Logger ─────────────────────────────────────────────────────
    // Queues key events and flushes them one-by-one every 3s to avoid
    // hammering the server with hundreds of individual HTTP requests.
    logKey(keyValue, eventType, originalEvent) {
      if (this.stage !== 'exam' || !this.examAttemptId || !this.applicantId) return

      this._keyLogQueue.push({
        attempt_id:    this.examAttemptId,
        applicant_id:  this.applicantId,
        event_type:    eventType,
        key_value:     keyValue,
        ctrl_key:      originalEvent?.ctrlKey  ?? false,
        shift_key:     originalEvent?.shiftKey ?? false,
        alt_key:       originalEvent?.altKey   ?? false,
        meta_key:      originalEvent?.metaKey  ?? false,
        log_timestamp: new Date().toISOString()
      })

      // Start flush timer if not already running
      if (!this._keyLogFlushTimer) {
        this._keyLogFlushTimer = setInterval(() => {
          this._flushKeyLogs()
        }, 3000)
      }
    },
    showInlineMessage(text, type = 'error') {
  this.inlineMessage = { text, type }

  setTimeout(() => {
    this.inlineMessage = null
  }, 5000)
},

clearInlineMessage() {
  this.inlineMessage = null
},

    async _flushKeyLogs() {
      if (!this._keyLogQueue.length) return

      const batch = this._keyLogQueue.splice(0, this._keyLogQueue.length)

      // Send each log individually (server expects single-row inserts)
      for (const entry of batch) {
        try {
          await axiosInstance.post('/student/log-key', entry)
        } catch {
          // Silent — never disrupt the exam for a logging failure
        }
      }
    },

    enterFullscreen() {
      const el = document.documentElement
      setTimeout(() => {
        if (el.requestFullscreen)           el.requestFullscreen()
        else if (el.webkitRequestFullscreen) el.webkitRequestFullscreen()
        else if (el.mozRequestFullScreen)    el.mozRequestFullScreen()
        else if (el.msRequestFullscreen)     el.msRequestFullscreen()
      }, 100)
    },

    startRedirectCountdown() {
      this.redirectCountdown = 10
      this.redirectTimer = setInterval(() => {
        if (this.redirectCountdown > 0) {
          this.redirectCountdown--
        } else {
          clearInterval(this.redirectTimer)
          clearInterval(this._keyLogFlushTimer)
          localStorage.clear()
          window.location.href = '/'
        }
      }, 1000)
    },

  saveAnswersLocal() {
    if (!this.examAttemptId) return

      const data = {
      attempt_id: this.examAttemptId,
      answers: this.answers,
      timer: this.timer,
      currentIndex: this.currentIndex
      }

      localStorage.setItem(
      `exam_attempt_${this.examAttemptId}`,
      JSON.stringify(data)
      )
  },

    handleBlur() {
      if (this.stage === 'exam') {
        this.startOutsideCountdown('Window lost focus (5s exceeded)')
      }
    },

    handleVisibilityChange() {
      if (document.hidden && this.stage === 'exam') {
        this.startOutsideCountdown('Tab switch detected (5s exceeded)')
      } else if (!document.hidden && this.stage === 'exam') {
        this.cancelOutsideCountdown()
      }
    },

    detectSplitScreen() {
      if (this.stage !== 'exam' || this.isProcessingViolation) return
      const isFullscreen  = document.fullscreenElement !== null
      const screenWidth   = window.screen.width
      const screenHeight  = window.screen.height
      const windowWidth   = window.innerWidth
      const windowHeight  = window.innerHeight
      if (!isFullscreen) {
        this.recoverFullscreen(100)
        return
      }
      const widthRatio  = windowWidth  / screenWidth
      const heightRatio = windowHeight / screenHeight
      if (widthRatio < 0.95 || heightRatio < 0.95) {
        this.recoverFullscreen(100)
      }
    },

    handleFullscreenChange() {
      if (this.stage === 'exam' && !document.fullscreenElement && !this.isProcessingViolation) {
        this.isProcessingViolation = true
        
        // Show warning immediately when fullscreen is exited
        this.violationCount++
        if (this.violationCount >= this.maxViolations) {
          this.forceExit('Exited fullscreen mode (attempted to exit exam)')
          return
        }
        
        const left = this.maxViolations - this.violationCount
        this.showInlineMessage(
          `⚠️ Warning ${this.violationCount}/${this.maxViolations}: Fullscreen exited. You have ${left} attempt(s) left.`,
          'warning'
        )
        
        setTimeout(() => {
          this.recoverFullscreen(100)
          this.isProcessingViolation = false
        }, 300)
      }
    },

    startOutsideCountdown(reason) {
      if (this.isOutsideScreen || this.stage !== 'exam') return

      this.isOutsideScreen  = true
      this.outsideCountdown = 5

      this.outsideTimer = setInterval(() => {
        this.outsideCountdown--

        if (this.outsideCountdown <= 0) {
          clearInterval(this.outsideTimer)
          this.outsideTimer    = null
          this.isOutsideScreen = false
          this.forceExit(reason)
        }
      }, 1000)
    },

    cancelOutsideCountdown() {
      if (!this.isOutsideScreen) return

      clearInterval(this.outsideTimer)
      this.outsideTimer    = null
      this.isOutsideScreen = false

      // Came back in time → normal warning
      this.handleViolation('Window lost focus (returned in time)')
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
      this.isOutsideScreen = false
      clearInterval(this.interval)
      clearInterval(this._keyLogFlushTimer)
      this._keyLogFlushTimer = null

      // Flush remaining key logs before submitting
      try {
  await this._flushKeyLogs()
} catch (e) {
  console.warn("Key log flush failed")
}

      // Fill unanswered questions
      this.answers = this.questions.map((q, index) => {
        if (this.answers[index]) return this.answers[index]
        return { question_id: q.Question_Id, selected_option: '' }
      })

      this.stage         = 'finished'
      this.finishMessage = `Exam forcibly ended.\nReason: ${reason}\n\nTotal Violations: ${this.violationCount}/${this.maxViolations}`

      window.removeEventListener('beforeunload', this.preventRefresh)

      try {
        const res = await axiosInstance.post('/student/submit', {
          applicant_id:       this.applicantId,
          exam_paper_id:      this.exam.Exam_Paper_Id,
          answers:            this.answers,
          attempt_id:         this.examAttemptId,
          is_restricted:      true,
          restriction_reason: reason
        })
        this.attemptId = res.data.Attempt_Id || this.examAttemptId
      } catch (err) {
        console.error('❌ Restriction submission failed:', err)
        this.attemptId = this.examAttemptId || 'N/A'
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

    // ─── handleKeydown ────────────────────────────────────────────────────────
    handleKeydown(event) {
      if (this.stage !== 'exam') return

      const key   = event.key
      const ctrl  = event.ctrlKey
      const shift = event.shiftKey
      const meta  = event.metaKey

      // ── Arrow / Enter navigation for MCQ/TF ─────────────────────────────────
      const qType = this.currentQuestion?.Question_Type
      if (['MCQ', 'TF'].includes(qType)) {
        if (['ArrowUp', 'ArrowDown'].includes(key)) {
          event.preventDefault()
          this.navigateOptions(key === 'ArrowUp' ? -1 : 1)
          return
        }
        if (key === 'Enter') {
          event.preventDefault()
          this.handleEnterKey()
          return
        }
      }

      // ── ESC — warning violation ──────────────────────────────────────────────
      if (key === 'Escape') {
        event.preventDefault()
        event.stopPropagation()
        this.logKey('Escape', 'warning', event)
        // Note: Violation counting is handled by handleFullscreenChange
        // This just prevents the default ESC behavior and logs it
        return
      }

      // ── PrintScreen / Mac screenshot — warning ───────────────────────────────
      if (key === 'PrintScreen' || (meta && shift && ['3', '4', '5'].includes(key))) {
        event.preventDefault()
        this.logKey('PrintScreen', 'warning', event)
        return
      }

      // ── F12 — blocked ────────────────────────────────────────────────────────
      if (key === 'F12') {
        event.preventDefault()
        this.logKey('F12', 'blocked', event)
        return
      }

      // ── Ctrl+Shift+I / C / J — DevTools — blocked ───────────────────────────
      if (ctrl && shift && ['I', 'C', 'J'].includes(key)) {
        event.preventDefault()
        this.logKey(`Ctrl+Shift+${key}`, 'blocked', event)
        return
      }

      // ── Ctrl+U — view source — blocked ───────────────────────────────────────
      if (ctrl && key === 'u') {
        event.preventDefault()
        this.logKey('Ctrl+U', 'blocked', event)
        return
      }

      // ── Ctrl+Tab — tab switch — blocked ──────────────────────────────────────
      if (ctrl && key === 'Tab') {
        event.preventDefault()
        this.logKey('Ctrl+Tab', 'blocked', event)
        return
      }

      // ── F5 / Ctrl+R / Ctrl+Shift+R — refresh — blocked ───────────────────────
      if (
        key === 'F5' ||
        (ctrl && (key === 'r' || key === 'R')) ||
        (ctrl && shift && (key === 'r' || key === 'R'))
      ) {
        event.preventDefault()
        this.logKey(key === 'F5' ? 'F5' : (shift ? 'Ctrl+Shift+R' : 'Ctrl+R'), 'blocked', event)
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
        // For text-based questions, use handleNext logic
        const type = this.currentQuestion.Question_Type
        if (type === 'Fill' || type === 'OneWord') {
          if (!this.textAnswer.trim()) {
            this.showInlineMessage('⚠️ Please provide an answer', 'warning')
            return
          }
          // Save the answer
          this.answers[this.currentIndex] = {
            question_id: this.currentQuestion.Question_Id,
            selected_option: this.textAnswer.trim()
          }
          this.saveAnswersLocal()
        }
        
        // Check if it's the last question
        const isLastQuestion = this.currentIndex + 1 === this.questions.length
        if (isLastQuestion) {
          // Check if all answers are filled
          const anyUnanswered = this.answers.some(ans => ans === null)
          if (anyUnanswered) {
            this.questions.forEach((_, idx) => {
              if (this.answers[idx] === null && !this.visitedQuestions.includes(idx)) {
                this.visitedQuestions.push(idx)
              }
            })
            setTimeout(() => this.showInlineMessage('⚠️ Please answer all questions.', 'warning'), 100)
            return
          }
          // Show confirmation modal
          if (this.$refs.examInterface) {
            this.$refs.examInterface.showSubmissionConfirmation()
          }
        } else {
          // Regular next question - use handleNext
          this.handleNext()
        }
      } else {
        this.showInlineMessage('⚠️ Select or enter an answer first', 'warning')
      }
    },

    selectOption(key) {
      this.selectedOption = key
      this.keyboardSelectedOption = null
      this.clearInlineMessage()

      // save immediately
      this.answers[this.currentIndex] = {
        question_id: this.currentQuestion.Question_Id,
        selected_option: key
      }

      this.saveAnswersLocal()
    },
    goBackToEntry() {
      this.stage        = 'enter'
      this.examIdError  = false
      this.clearInlineMessage()
      this.exam         = null
      this.questions    = []
      this.examAttemptId = null
      this.currentIndex = 0
      this.answers      = []
      this.visitedQuestions = []
    },

    async fetchExam(examId) {
      this.examId = examId
      try {
        this.examIdError = false
        this.clearInlineMessage()

        const res = await axiosInstance.post(`/student/exam/${this.examId}`, {
          applicant_id: this.applicantId
        })

        this.exam          = res.data.exam
        this.questions     = res.data.questions
        this.answers       = new Array(this.questions.length).fill(null)
        this.examAttemptId = res.data.attempt_id || null

        this.timer = res.data.exam.Remaining_Seconds !== undefined
          ? res.data.exam.Remaining_Seconds
          : this.exam.Duration_Minutes * 60

        this.stage = 'instructions'
        this.clearInlineMessage()
      } catch (error) {
        this.examIdError = true
        if (error.response) {
          const status    = error.response.status
          const errorData = error.response.data
          switch (status) {
            case 425:
              this.showInlineMessage(errorData.error || 'Exam has not started yet. Please wait until the scheduled time.', 'error')
              break
            case 410:
              this.showInlineMessage(errorData.error || 'Exam entry time has expired. You cannot start the exam after 10 minutes of exam start time.', 'error')
              break
            case 403:
              this.showInlineMessage(errorData.error || 'Access Denied: You are not assigned to this exam', 'error')
              break
            case 409:
              this.showInlineMessage(errorData.error || 'You have already attempted this exam', 'error')
              break
            case 404:
              this.showInlineMessage('Invalid Exam ID', 'error')
              break
            default:
              this.showInlineMessage(errorData.error || 'Failed to load exam. Please try again.', 'error')
          }
        } else {
          this.showInlineMessage('Network error. Please check your connection.', 'error')
        }
      }
    },

    async startExam() {
      try {
        const res = await axiosInstance.post('/student/start-exam', {
          applicant_id: this.applicantId,
          exam_id:      this.exam.Exam_Id
        })

        if (res.data?.attempt_id) {
          this.examAttemptId = res.data.attempt_id
        }

        this.stage = 'exam'
        const saved = localStorage.getItem(`exam_attempt_${this.examAttemptId}`)

        if (saved) {
          const parsed = JSON.parse(saved)

          this.answers = parsed.answers || this.answers
          this.timer = parsed.timer || this.timer
          this.currentIndex = parsed.currentIndex || 0
        }
        this.enterFullscreen()
        this.autoSaveTimer = setInterval(() => {
        this.saveAnswersLocal()
        }, 10000)

        this.interval = setInterval(() => {
          if (this.timer > 0) {
            this.timer--
            if (this.timer === 300) this.showInlineMessage('⚠️ Only 5 minutes remaining!', 'warning')
            else if (this.timer === 60) this.showInlineMessage('🚨 Only 1 minute remaining!', 'warning')
          } else {
            clearInterval(this.interval)
            this.handleTimerFinish()
          }
        }, 1000)

        setTimeout(() => {
          if (this.stage === 'exam' && !document.fullscreenElement) this.enterFullscreen()
        }, 1000)
      } catch (err) {
        console.error('Failed to start exam attempt:', err)
        this.showInlineMessage('Failed to start exam. Please try again.', 'error')
      }
    },

    handleTimerFinish() {
      this.answers = this.answers.map((ans, idx) => {
        if (ans === null) return { question_id: this.questions[idx].Question_Id, selected_option: '' }
        return ans
      })
      this.finishExam('⏰ Time is up!\nYour exam has been auto-submitted.')
    },

    handleNext() {
      const type = this.currentQuestion.Question_Type
      let value  = null

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
        question_id:     this.currentQuestion.Question_Id,
        selected_option: value
      }
      this.saveAnswersLocal()

      const last = this.currentIndex + 1 === this.questions.length
      if (last) {
        const anyUnanswered = this.answers.some(ans => ans === null)
        if (anyUnanswered) {
          this.questions.forEach((_, idx) => {
            if (this.answers[idx] === null && !this.visitedQuestions.includes(idx)) {
              this.visitedQuestions.push(idx)
            }
          })
          setTimeout(() => this.showInlineMessage('⚠️ Please answer all questions.', 'warning'), 100)
          return
        }
        clearInterval(this.interval)
        this.finishExam('✅ All questions submitted!')
      } else {
        this.selectedOption        = null
        this.textAnswer            = ''
        this.keyboardSelectedOption = null
        this.clearInlineMessage()
        this.currentIndex++
        this.loadCurrentAnswer()
      }
    },

    loadCurrentAnswer() {
      const ans  = this.answers[this.currentIndex]
      const type = this.currentQuestion.Question_Type
      if (ans) {
        if (type === 'MCQ' || type === 'TF') this.selectedOption = ans.selected_option
        else this.textAnswer = ans.selected_option
      } else {
        this.selectedOption = null
        this.textAnswer     = ''
      }
      this.keyboardSelectedOption = null
      this.clearInlineMessage()
    },

    jumpToQuestion(idx) {
      if (!this.visitedQuestions.includes(this.currentIndex)) {
        this.visitedQuestions.push(this.currentIndex)
      }
      this.currentIndex = idx
      this.loadCurrentAnswer()
    },

  async finishExam(msg) {

  this.questions.forEach((_, idx) => {
    if (this.answers[idx] === null && !this.visitedQuestions.includes(idx)) {

      this.visitedQuestions.push(idx)

      this.answers[idx] = {
        question_id: this.questions[idx].Question_Id,
        selected_option: ''
      }

    }
  })

  window.removeEventListener('beforeunload', this.preventRefresh)

  clearInterval(this.interval)

  if (this.autoSaveTimer) {
    clearInterval(this.autoSaveTimer)
  }

  if (this._keyLogFlushTimer) {
    clearInterval(this._keyLogFlushTimer)
    this._keyLogFlushTimer = null
  }

  try {
    await this._flushKeyLogs()
  } catch {
    console.warn("Key log flush failed")
  }

  let retries = 3
  let submitted = false

  while (retries > 0 && !submitted) {

    try {

      const res = await axiosInstance.post('/student/submit', {
        applicant_id: this.applicantId,
        exam_paper_id: this.exam.Exam_Paper_Id,
        answers: this.answers,
        attempt_id: this.examAttemptId
      })

      this.attemptId = res.data.Attempt_Id || this.examAttemptId || 'N/A'
      submitted = true

      localStorage.removeItem(`exam_attempt_${this.examAttemptId}`)

      this.stage = 'finished'
      this.finishMessage = msg

      const email = localStorage.getItem('student_email')

      if (email) {
        try {
          await axiosInstance.post('/logout', { email, role: 'Student' })
        } catch {
          console.warn("Logout failed but exam submitted.")
        }
      }

  // =========================
  // LOGOUT (ALWAYS EXECUTE)
  // =========================
  try {
    await axiosInstance.post('/logout')
  } catch (err) {
    console.error('Logout error:', err)
  }

  // =========================
  // REDIRECT
  // =========================
  this.startRedirectCountdown()

} catch (err) {

  retries--

  console.error("Submission failed, retrying...", retries)

  if (!err.response) {
  this.showInlineMessage("⚠️ Internet connection lost. Retrying...", "warning")
} else {
  this.showInlineMessage("⚠️ Server error. Retrying submission...", "warning")
}

  await new Promise(resolve => setTimeout(resolve, 5000))

}
  }
  if (!submitted) {
  this.showInlineMessage(
    "❌ Could not submit exam. Please try again or contact admin.",
    "error"
  )
}
  }
  }  
}
</script>

<style scoped>
/* Logout button pop-in */
@keyframes popIn {
  0%   { opacity: 0; transform: scale(0.5); }
  70%  { transform: scale(1.1); }
  100% { opacity: 1; transform: scale(1); }
}

.logout-btn {
  animation: popIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) 1.2s both;
}

/* Hint label fade in/out */
@keyframes hintFade {
  0%   { opacity: 0; transform: translateY(-50%) translateX(6px); }
  15%  { opacity: 1; transform: translateY(-50%) translateX(0); }
  80%  { opacity: 1; }
  100% { opacity: 0; }
}

.logout-hint {
  animation: hintFade 2s ease forwards;
}
</style>
