<template>
  <div class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/40" @click.self="$emit('close')">
    <div class="bg-white rounded-lg shadow-xl w-full max-w-5xl max-h-[90vh] overflow-hidden flex flex-col m-4 border border-gray-300">

      <!-- Header -->
      <div class="bg-gray-800 px-5 py-4 flex items-center justify-between">
        <div>
          <h2 class="text-lg font-semibold text-white">Exam Activity Report</h2>
          <p class="text-gray-300 text-sm">{{ examName }}</p>
          <p class="text-gray-400 text-xs">{{ studentName }} &bull; {{ studentEmail }}</p>
        </div>
        <button @click="$emit('close')" class="text-gray-400 hover:text-white p-1.5 rounded hover:bg-gray-700 transition">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex-1 flex items-center justify-center bg-gray-50">
        <div class="text-center">
          <div class="w-8 h-8 border-2 border-gray-400 border-t-gray-800 rounded-full animate-spin mx-auto mb-2"></div>
          <p class="text-gray-500 text-sm">Loading...</p>
        </div>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="flex-1 flex items-center justify-center bg-gray-50">
        <div class="text-center">
          <p class="text-red-600 text-sm mb-3">{{ error }}</p>
          <button @click="fetchAll" class="px-4 py-2 bg-gray-800 text-white rounded text-sm hover:bg-gray-700">Retry</button>
        </div>
      </div>

      <!-- Content -->
      <div v-else class="flex-1 overflow-y-auto bg-gray-50">

        <!-- Warnings Summary Bar -->
        <div v-if="warnings.length > 0" class="bg-amber-50 border-b border-amber-300 px-5 py-3">
          <p class="text-xs font-semibold text-amber-800 mb-2">Warnings Received ({{ warnings.length }})</p>
          <div class="flex flex-wrap gap-2">
            <span v-for="(w, i) in warnings" :key="i"
              class="text-xs bg-white border px-2.5 py-1 rounded font-medium"
              :class="i === warnings.length - 1 ? 'border-red-500 text-red-700 font-semibold' : 'border-amber-400 text-amber-800'">
              {{ i + 1 }}. {{ w.Reason }}
              <span v-if="i === warnings.length - 1" class="ml-1 text-red-600">(Restricted)</span>
            </span>
          </div>
        </div>

        <!-- No data at all -->
        <div v-if="questions.length === 0" class="flex items-center justify-center py-16 text-gray-400 text-sm">
          No activity data found for this attempt.
        </div>

        <!-- Per-Question Cards -->
        <div class="p-5 space-y-4">
          <div v-for="(q, idx) in questions" :key="q.question_id" class="bg-white border border-gray-200 rounded overflow-hidden">

            <!-- Question Header -->
            <div class="bg-gray-100 px-4 py-2.5 border-b border-gray-200 flex items-center gap-2">
              <span class="bg-gray-800 text-white text-xs font-semibold px-2 py-0.5 rounded">Q{{ idx + 1 }}</span>
              <span class="text-xs text-gray-500 bg-gray-200 px-2 py-0.5 rounded">{{ q.question_type }}</span>
              <span class="text-sm text-gray-700 font-medium ml-1">{{ q.question_text }}</span>
            </div>

            <div class="p-4 space-y-3">

              <!-- Answer Given (from actual answers table) -->
              <div class="flex items-start gap-3 p-3 bg-gray-50 border border-gray-200 rounded">
                <span class="text-xs font-semibold text-gray-500 w-24 shrink-0 pt-0.5">Answer Given</span>
                <span class="text-sm text-gray-800 font-medium">
                  {{ q.answer_given || '— Not answered —' }}
                </span>
                <span v-if="q.answer_given" class="ml-auto text-xs shrink-0"
                  :class="q.is_correct ? 'text-green-600 font-semibold' : 'text-red-500 font-semibold'">
                  {{ q.is_correct ? '✓ Correct' : '✗ Wrong' }}
                </span>
              </div>

              <!-- Mouse Selections -->
              <div v-if="q.mouse_clicks > 0" class="flex items-center gap-3 p-3 bg-blue-50 border border-blue-200 rounded">
                <span class="text-xs font-semibold text-blue-700 w-24 shrink-0">Mouse Clicks</span>
                <span class="text-sm text-blue-800">{{ q.mouse_clicks }} click{{ q.mouse_clicks > 1 ? 's' : '' }} recorded</span>
              </div>

              <!-- Suspicious Keys -->
              <div v-if="q.suspicious.length > 0" class="p-3 bg-red-50 border border-red-200 rounded">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-xs font-semibold text-red-700">Suspicious Keys ({{ q.suspicious.length }})</span>
                </div>
                <!-- Show first 10 -->
                <div class="space-y-1">
                  <div v-for="(s, si) in (expandedSuspicious[q.question_id] ? q.suspicious : q.suspicious.slice(0, 10))"
                    :key="si"
                    class="flex items-center justify-between bg-white border border-red-200 rounded px-3 py-1.5">
                    <code class="text-xs text-red-800 font-mono font-semibold">{{ s.label }}</code>
                    <span class="text-xs text-gray-500 ml-4">{{ s.type }}</span>
                  </div>
                </div>
                <!-- More button -->
                <button v-if="q.suspicious.length > 10 && !expandedSuspicious[q.question_id]"
                  @click="expandedSuspicious[q.question_id] = true"
                  class="mt-2 text-xs text-red-600 hover:text-red-800 font-medium underline">
                  + {{ q.suspicious.length - 10 }} more
                </button>
                <button v-else-if="expandedSuspicious[q.question_id]"
                  @click="expandedSuspicious[q.question_id] = false"
                  class="mt-2 text-xs text-gray-500 hover:text-gray-700 font-medium underline">
                  Show less
                </button>
              </div>

              <!-- No suspicious -->
              <div v-else class="flex items-center gap-2 px-3 py-2 bg-gray-50 border border-gray-200 rounded">
                <span class="text-xs text-gray-400">No suspicious activity on this question</span>
              </div>

            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="bg-white border-t border-gray-200 px-5 py-3 flex justify-end">
        <button @click="$emit('close')" class="px-5 py-2 bg-gray-800 text-white rounded text-sm hover:bg-gray-700 font-medium transition">
          Close
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from '../utils/axiosInstance'

const props = defineProps({
  attemptId: { type: Number, required: true }
})
const emit = defineEmits(['close'])

const loading    = ref(true)
const error      = ref('')
const examName   = ref('')
const studentName = ref('')
const studentEmail = ref('')
const warnings   = ref([])   // from restricted_attempts
const questions  = ref([])   // merged: keystroke + answers
const expandedSuspicious = reactive({})

// ─── Label a suspicious keystroke ────────────────────────────────────────────
const suspiciousLabel = (ks) => {
  const combo = (ks.combination || '').toLowerCase()
  if (combo.includes('ctrl+c') || combo.includes('cmd+c')) return { label: ks.combination, type: 'Copy Attempt' }
  if (combo.includes('ctrl+v') || combo.includes('cmd+v')) return { label: ks.combination, type: 'Paste Attempt' }
  if (combo.includes('ctrl+x') || combo.includes('cmd+x')) return { label: ks.combination, type: 'Cut Attempt' }
  if (combo.includes('ctrl+tab'))                           return { label: ks.combination, type: 'Tab Switch' }
  if (combo.includes('ctrl+r') || combo.includes('ctrl+shift+r')) return { label: ks.combination, type: 'Refresh Attempt' }
  if (combo.includes('ctrl+shift+i') || combo.includes('ctrl+shift+j') || combo.includes('ctrl+shift+c')) return { label: ks.combination, type: 'DevTools' }
  if (combo.includes('ctrl+u'))                             return { label: ks.combination, type: 'View Source' }
  if (combo.includes('ctrl+a'))                             return { label: ks.combination, type: 'Select All' }
  if (ks.key === 'F12')                                     return { label: 'F12', type: 'DevTools Key' }
  if (ks.key === 'PrintScreen')                             return { label: 'PrintScreen', type: 'Screenshot' }
  if (ks.key === 'Escape')                                  return { label: 'Escape', type: 'Escape Key' }
  if (['F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11'].includes(ks.key)) return { label: ks.key, type: 'Function Key' }
  if (ks.ctrl || ks.alt || ks.meta)                        return { label: ks.combination || ks.key, type: 'Key Combination' }
  return { label: ks.key, type: 'Other' }
}

// ─── Fetch everything ─────────────────────────────────────────────────────────
const fetchAll = async () => {
  loading.value = true
  error.value   = ''

  try {
    const email = localStorage.getItem('email') || ''
    const role  = localStorage.getItem('active_role') || ''

    const [keystrokeRes, answersRes, warningsRes] = await Promise.all([
      axios.get(`/keystroke/logs/${props.attemptId}`),
      axios.get(`/answers/${props.attemptId}`, { params: { email, role } }),
      axios.get(`/keystroke/warnings/${props.attemptId}`)
    ])

    if (!keystrokeRes.data.success) {
      error.value = keystrokeRes.data.message || 'Failed to load data'
      return
    }

    examName.value    = keystrokeRes.data.exam_name
    studentName.value = keystrokeRes.data.student_name
    studentEmail.value = keystrokeRes.data.student_email

    // Warnings from restricted_attempts
    warnings.value = warningsRes.data.success ? warningsRes.data.warnings : []

    // Build answer map: question_id → answer info
    const answerMap = {}
    if (answersRes.data.success) {
      answersRes.data.answers.forEach(a => {
        let given = ''
        if (a.Question_Type === 'MCQ' || a.Question_Type === 'TF') {
          const optMap = { A: a.Option_A, B: a.Option_B, C: a.Option_C, D: a.Option_D }
          given = a.Selected_Option_Id ? `${a.Selected_Option_Id}. ${optMap[a.Selected_Option_Id] || ''}` : ''
        } else {
          given = a.Answer_Text || ''
        }
        const isCorrect = a.Selected_Option_Id
          ? a.Selected_Option_Id === a.Correct_Answer
          : (a.Answer_Text || '').trim().toLowerCase() === (a.Correct_Answer || '').trim().toLowerCase()

        answerMap[a.Question_Id] = { given, isCorrect }
      })
    }

    // Merge keystroke logs with answers
    questions.value = keystrokeRes.data.logs.map(q => {
      const ans = answerMap[q.question_id] || {}
      const suspicious = []
      let mouse_clicks = 0

      q.keystrokes.forEach(ks => {
        // Count mouse clicks (log_type = 'mouse')
        if (ks.log_type === 'mouse') {
          mouse_clicks++
          return
        }
        // Suspicious: combinations or special keys (NOT plain alphabets/numbers)
        const isSuspicious =
          ks.ctrl || ks.alt || ks.meta ||
          ['F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12','PrintScreen','Escape'].includes(ks.key)

        if (isSuspicious) {
          suspicious.push(suspiciousLabel(ks))
        }
      })

      return {
        question_id:   q.question_id,
        question_text: q.question_text,
        question_type: q.question_type,
        answer_given:  ans.given || '',
        is_correct:    ans.isCorrect || false,
        mouse_clicks,
        suspicious
      }
    })

  } catch (e) {
    console.error(e)
    error.value = 'Failed to load activity data'
  } finally {
    loading.value = false
  }
}

onMounted(fetchAll)
</script>

<style scoped>
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #f3f4f6; }
::-webkit-scrollbar-thumb { background: #9ca3af; border-radius: 3px; }
</style>
