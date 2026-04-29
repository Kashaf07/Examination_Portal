<template>
  <div
    class="fixed inset-0 z-[9999] flex items-center justify-center backdrop-blur-sm"
    style="background: rgba(30, 27, 46, 0.55);"
    @click.self="$emit('close')"
  >
    <div class="bg-white rounded-2xl w-full max-w-5xl max-h-[90vh] overflow-hidden flex flex-col m-4"
      style="border: 1px solid #ddd8f5;">

      <!-- ── Header ── -->
      <div class="px-6 py-4 flex items-center justify-between flex-shrink-0"
        style="background: #fafafa; border-bottom: 1px solid #ebebeb;">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0"
            style="background: #f0f0f0; border: 1px solid #e0e0e0;">
            <svg class="w-5 h-5" fill="none" stroke="#534AB7" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round" viewBox="0 0 24 24">
              <rect x="2" y="3" width="20" height="14" rx="2"/>
              <path d="M8 21h8M12 17v4"/>
            </svg>
          </div>
          <div>
            <h2 class="text-base font-bold leading-tight" style="color: #26215C;">Exam Activity Report</h2>
            <p class="text-sm mt-0.5" style="color: #534AB7;">{{ examName }}</p>
            <p class="text-xs mt-0.5" style="color: #7c6fa0;">
              {{ studentName }} &bull; {{ studentEmail }}
            </p>
          </div>
        </div>
        <button @click="$emit('close')"
          class="w-8 h-8 rounded-lg flex items-center justify-center transition"
          style="background: #f0f0f0; border: 1px solid #e0e0e0;"
          onmouseover="this.style.background='#e4e4e4'"
          onmouseout="this.style.background='#f0f0f0'">
          <svg class="w-4 h-4" fill="none" stroke="#534AB7" stroke-width="2.5" stroke-linecap="round" viewBox="0 0 24 24">
            <path d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- ── Loading ── -->
      <div v-if="loading" class="flex-1 flex items-center justify-center" style="background:#f7f5ff;">
        <div class="text-center">
          <div class="w-9 h-9 rounded-full animate-spin mx-auto mb-3"
            style="border: 3px solid #e8e2f8; border-top-color: #7c3aed;"></div>
          <p class="text-sm" style="color:#888;">Loading activity data...</p>
        </div>
      </div>

      <!-- ── Error ── -->
      <div v-else-if="error" class="flex-1 flex items-center justify-center" style="background:#f7f5ff;">
        <div class="text-center">
          <div class="w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3"
            style="background:#fee2e2;">
            <svg class="w-6 h-6" fill="none" stroke="#dc2626" stroke-width="2" stroke-linecap="round" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
          </div>
          <p class="text-sm mb-3" style="color:#dc2626;">{{ error }}</p>
          <button @click="fetchAll"
            class="px-5 py-2 rounded-lg text-sm font-semibold text-white transition"
            style="background: linear-gradient(120deg,#3a5bd9,#7c3aed);">
            Retry
          </button>
        </div>
      </div>

      <!-- ── Content ── -->
      <div v-else class="flex-1 overflow-y-auto" style="background:#f7f5ff;">

        <!-- Stats Summary Bar -->
        <div class="px-6 py-3 flex flex-wrap gap-2 flex-shrink-0"
          style="background:#f3f0ff; border-bottom: 1px solid #e0d9f7;">
          <div class="flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold"
            style="background:#fff; border:1px solid #d8d0f5; color:#534AB7;">
            <span class="w-2 h-2 rounded-full inline-block" style="background:#534AB7;"></span>
            {{ questions.length }} Question{{ questions.length !== 1 ? 's' : '' }}
          </div>
          <div v-if="totalSuspicious > 0"
            class="flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold"
            style="background:#fff5f5; border:1px solid #fecaca; color:#991b1b;">
            <span class="w-2 h-2 rounded-full inline-block" style="background:#dc2626;"></span>
            {{ totalSuspicious }} Suspicious Key{{ totalSuspicious !== 1 ? 's' : '' }}
          </div>
          <div v-if="warnings.length > 0"
            class="flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold"
            style="background:#fffbeb; border:1px solid #fde68a; color:#92400e;">
            <span class="w-2 h-2 rounded-full inline-block" style="background:#d97706;"></span>
            {{ warnings.length }} Warning{{ warnings.length !== 1 ? 's' : '' }}
          </div>
          <div v-if="totalMouseClicks > 0"
            class="flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold"
            style="background:#f0fdf4; border:1px solid #bbf7d0; color:#065f46;">
            <span class="w-2 h-2 rounded-full inline-block" style="background:#059669;"></span>
            {{ totalMouseClicks }} Mouse Click{{ totalMouseClicks !== 1 ? 's' : '' }}
          </div>
        </div>

        <!-- Warnings Bar -->
        <div v-if="warnings.length > 0" class="px-6 py-3 flex-shrink-0"
          style="background:#fffbeb; border-bottom:1px solid #fde68a;">
          <p class="text-xs font-bold mb-2 flex items-center gap-1.5" style="color:#92400e;">
            <svg class="w-3.5 h-3.5" fill="none" stroke="#d97706" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round" viewBox="0 0 24 24">
              <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
              <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>
            Warnings Received ({{ warnings.length }})
          </p>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="(w, i) in warnings" :key="i"
              class="text-xs px-2.5 py-1 rounded-lg font-medium"
              :style="i === warnings.length - 1
                ? 'background:#fff; border:1px solid #ef4444; color:#dc2626; font-weight:700;'
                : 'background:#fff; border:1px solid #fbbf24; color:#92400e;'">
              {{ i + 1 }}. {{ w.Reason }}
              <span v-if="i === warnings.length - 1" style="color:#dc2626;"> (Restricted)</span>
            </span>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="questions.length === 0"
          class="flex flex-col items-center justify-center py-20 gap-3">
          <div class="w-14 h-14 rounded-full flex items-center justify-center"
            style="background:#e8e2f8;">
            <svg class="w-7 h-7" fill="none" stroke="#7c3aed" stroke-width="1.5" stroke-linecap="round"
              stroke-linejoin="round" viewBox="0 0 24 24">
              <path d="M9 12h6M9 16h6M14 3H6a2 2 0 00-2 2v14a2 2 0 002 2h12a2 2 0 002-2V8z"/>
              <polyline points="14 3 14 8 19 8"/>
            </svg>
          </div>
          <p class="text-sm" style="color:#9ca3af;">No activity data found for this attempt.</p>
        </div>

        <!-- Per-Question Cards -->
        <div class="p-5 space-y-3">
          <div v-for="(q, idx) in questions" :key="q.question_id"
            class="rounded-xl overflow-hidden"
            style="background:#fff; border:1px solid #e8e2f8;">

            <!-- Question Header -->
            <div class="px-4 py-2.5 flex items-center gap-2 flex-wrap"
              style="background:#f3f0ff; border-bottom:1px solid #e8e2f8;">
              <span class="text-xs font-bold px-2.5 py-0.5 rounded-md text-white"
                style="background:#534AB7;">Q{{ idx + 1 }}</span>
              <span class="text-xs font-semibold px-2.5 py-0.5 rounded-md"
                style="background:#e8e2f8; color:#534AB7;">{{ q.question_type }}</span>
              <span class="text-sm font-medium" style="color:#3C3489;">{{ q.question_text }}</span>
            </div>

            <div class="p-4 space-y-2.5">

              <!-- Answer Given -->
              <div class="flex items-start gap-3 rounded-lg px-3 py-2.5"
                style="background:#f7f5ff; border:1px solid #e8e2f8;">
                <span class="text-xs font-bold flex-shrink-0 w-24 pt-0.5" style="color:#534AB7;">Answer Given</span>
                <span class="text-sm flex-1 font-medium" style="color:#26215C;">
                  {{ q.answer_given || '— Not answered —' }}
                </span>
                <span v-if="q.answer_given !== undefined"
                  class="text-xs font-bold px-2.5 py-0.5 rounded-full flex-shrink-0"
                  :style="q.is_correct
                    ? 'background:#dcfce7; color:#166534;'
                    : 'background:#fee2e2; color:#991b1b;'">
                  {{ q.is_correct ? '✓ Correct' : '✗ Wrong' }}
                </span>
              </div>

              <!-- Mouse Clicks -->
              <div v-if="q.mouse_clicks > 0"
                class="flex items-center gap-3 rounded-lg px-3 py-2.5"
                style="background:#eff6ff; border:1px solid #bfdbfe;">
                <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="#2563eb" stroke-width="2"
                  stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                  <path d="M12 2a7 7 0 017 7v3a7 7 0 01-14 0V9a7 7 0 017-7z"/>
                  <line x1="12" y1="11" x2="12" y2="15"/>
                </svg>
                <span class="text-xs font-bold w-24 flex-shrink-0" style="color:#1d4ed8;">Mouse Clicks</span>
                <span class="text-sm" style="color:#1e40af;">
                  {{ q.mouse_clicks }} click{{ q.mouse_clicks > 1 ? 's' : '' }} recorded
                </span>
              </div>

              <!-- Suspicious Keys -->
              <div v-if="q.suspicious.length > 0"
                class="rounded-lg px-3 py-2.5"
                style="background:#fff5f5; border:1px solid #fecaca;">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-xs font-bold flex items-center gap-1.5" style="color:#991b1b;">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="#dc2626" stroke-width="2"
                      stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                      <circle cx="12" cy="12" r="10"/>
                      <line x1="12" y1="8" x2="12" y2="12"/>
                      <line x1="12" y1="16" x2="12.01" y2="16"/>
                    </svg>
                    Suspicious Keys ({{ q.suspicious.length }})
                  </span>
                </div>
                <div class="space-y-1">
                  <div
                    v-for="(s, si) in (expandedSuspicious[q.question_id] ? q.suspicious : q.suspicious.slice(0, 10))"
                    :key="si"
                    class="flex items-center justify-between rounded-lg px-3 py-1.5"
                    style="background:#fff; border:1px solid #fecaca;">
                    <code class="text-xs font-mono font-bold" style="color:#991b1b;">{{ s.label }}</code>
                    <span class="text-xs" style="color:#9ca3af;">{{ s.type }}</span>
                  </div>
                </div>
                <button
                  v-if="q.suspicious.length > 10 && !expandedSuspicious[q.question_id]"
                  @click="expandedSuspicious[q.question_id] = true"
                  class="mt-2 text-xs font-semibold underline" style="color:#dc2626;">
                  + {{ q.suspicious.length - 10 }} more
                </button>
                <button
                  v-else-if="expandedSuspicious[q.question_id]"
                  @click="expandedSuspicious[q.question_id] = false"
                  class="mt-2 text-xs font-semibold underline" style="color:#9ca3af;">
                  Show less
                </button>
              </div>

              <!-- Clean -->
              <div v-else
                class="flex items-center gap-2 rounded-lg px-3 py-2.5"
                style="background:#f7f5ff; border:1px solid #e8e2f8;">
                <div class="w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0"
                  style="background:#d1fae5;">
                  <svg class="w-3 h-3" fill="none" stroke="#059669" stroke-width="2.5"
                    stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                    <polyline points="20 6 9 17 4 12"/>
                  </svg>
                </div>
                <span class="text-xs" style="color:#9ca3af;">No suspicious activity on this question</span>
              </div>

            </div>
          </div>
        </div>

      </div>

      <!-- ── Footer ── -->
      <div class="px-6 py-3 flex justify-end flex-shrink-0"
        style="background:#fff; border-top:1px solid #e8e2f8;">
        <button @click="$emit('close')"
          class="px-6 py-2 rounded-xl text-sm font-semibold text-white transition"
          style="background: linear-gradient(120deg, #3a5bd9 0%, #7c3aed 100%);">
          Close
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import axios from '../utils/axiosInstance'

const props = defineProps({
  attemptId: { type: Number, required: true }
})
const emit = defineEmits(['close'])

const loading       = ref(true)
const error         = ref('')
const examName      = ref('')
const studentName   = ref('')
const studentEmail  = ref('')
const warnings      = ref([])
const questions     = ref([])
const expandedSuspicious = reactive({})

const totalSuspicious = computed(() => questions.value.reduce((acc, q) => acc + q.suspicious.length, 0))
const totalMouseClicks = computed(() => questions.value.reduce((acc, q) => acc + q.mouse_clicks, 0))

const suspiciousLabel = (ks) => {
  const combo = (ks.combination || '').toLowerCase()
  if (combo.includes('ctrl+c') || combo.includes('cmd+c')) return { label: ks.combination, type: 'Copy Attempt' }
  if (combo.includes('ctrl+v') || combo.includes('cmd+v')) return { label: ks.combination, type: 'Paste Attempt' }
  if (combo.includes('ctrl+x') || combo.includes('cmd+x')) return { label: ks.combination, type: 'Cut Attempt' }
  if (combo.includes('ctrl+tab'))                          return { label: ks.combination, type: 'Tab Switch' }
  if (combo.includes('ctrl+r') || combo.includes('ctrl+shift+r')) return { label: ks.combination, type: 'Refresh Attempt' }
  if (combo.includes('ctrl+shift+i') || combo.includes('ctrl+shift+j') || combo.includes('ctrl+shift+c'))
                                                           return { label: ks.combination, type: 'DevTools' }
  if (combo.includes('ctrl+u'))                            return { label: ks.combination, type: 'View Source' }
  if (combo.includes('ctrl+a'))                            return { label: ks.combination, type: 'Select All' }
  if (ks.key === 'F12')                                    return { label: 'F12',          type: 'DevTools Key' }
  if (ks.key === 'PrintScreen')                            return { label: 'PrintScreen',  type: 'Screenshot' }
  if (ks.key === 'Escape')                                 return { label: 'Escape',       type: 'Escape Key' }
  if (['F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11'].includes(ks.key))
                                                           return { label: ks.key,         type: 'Function Key' }
  if (ks.ctrl || ks.alt || ks.meta)                        return { label: ks.combination || ks.key, type: 'Key Combination' }
  return { label: ks.key, type: 'Other' }
}

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

    examName.value     = keystrokeRes.data.exam_name
    studentName.value  = keystrokeRes.data.student_name
    studentEmail.value = keystrokeRes.data.student_email
    warnings.value     = warningsRes.data.success ? warningsRes.data.warnings : []

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

    questions.value = keystrokeRes.data.logs.map(q => {
      const ans = answerMap[q.question_id] || {}
      const suspicious = []
      let mouse_clicks = 0
      q.keystrokes.forEach(ks => {
        if (ks.log_type === 'mouse') { mouse_clicks++; return }
        const isSuspicious =
          ks.ctrl || ks.alt || ks.meta ||
          ['F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12','PrintScreen','Escape'].includes(ks.key)
        if (isSuspicious) suspicious.push(suspiciousLabel(ks))
      })
      return {
        question_id:   q.question_id,
        question_text: q.question_text,
        question_type: q.question_type,
        answer_given:  ans.given ?? '',
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
::-webkit-scrollbar-track { background: #f3f0ff; }
::-webkit-scrollbar-thumb { background: #c4b5fd; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #a78bfa; }
</style>