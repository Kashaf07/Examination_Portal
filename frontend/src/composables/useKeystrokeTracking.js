import { ref, onMounted, onBeforeUnmount } from 'vue'
import axios from '../utils/axiosInstance'

export function useKeystrokeTracking() {
  const keystrokeQueue = ref([])
  const batchSize = 50
  const flushInterval = 10000
  let flushTimer = null

  // ─── Log a keyboard event ────────────────────────────────────────────────
  const logKeystroke = (attemptId, applicantId, questionId, event) => {
    if (!attemptId || !applicantId || !questionId) return

    const key     = event.key
    const code    = event.code
    const isCtrl  = event.ctrlKey
    const isAlt   = event.altKey
    const isShift = event.shiftKey
    const isMeta  = event.metaKey

    // Build combination string only when modifier keys are involved
    let combination = null
    if (isCtrl || isAlt || isMeta) {
      let combo = ''
      if (isCtrl)  combo += 'Ctrl+'
      if (isAlt)   combo += 'Alt+'
      if (isShift) combo += 'Shift+'
      if (isMeta)  combo += 'Cmd+'
      combo += (key && key.length === 1) ? key.toUpperCase() : (key || '')
      combination = combo
    }

    keystrokeQueue.value.push({
      attempt_id:      attemptId,
      applicant_id:    applicantId,
      question_id:     questionId,
      key_pressed:     key,
      key_code:        code,
      is_ctrl:         isCtrl,
      is_alt:          isAlt,
      is_shift:        isShift,
      is_meta:         isMeta,
      key_combination: combination,
      log_type:        'key',
      timestamp:       new Date().toISOString().slice(0, 19).replace('T', ' ')
    })

    if (keystrokeQueue.value.length >= batchSize) {
      flushKeystrokes()
    }
  }

  // ─── Log a mouse click (option selection) ────────────────────────────────
  const logMouseClick = (attemptId, applicantId, questionId, optionLabel) => {
    if (!attemptId || !applicantId || !questionId) return

    keystrokeQueue.value.push({
      attempt_id:      attemptId,
      applicant_id:    applicantId,
      question_id:     questionId,
      key_pressed:     optionLabel || 'click',
      key_code:        'MouseClick',
      is_ctrl:         false,
      is_alt:          false,
      is_shift:        false,
      is_meta:         false,
      key_combination: null,
      log_type:        'mouse',
      timestamp:       new Date().toISOString().slice(0, 19).replace('T', ' ')
    })

    if (keystrokeQueue.value.length >= batchSize) {
      flushKeystrokes()
    }
  }

  const flushKeystrokes = async () => {
    if (keystrokeQueue.value.length === 0) return
    const logsToSend = [...keystrokeQueue.value]
    keystrokeQueue.value = []
    try {
      await axios.post('/keystroke/log', { logs: logsToSend })
    } catch (err) {
      console.error('❌ Failed to send keystroke logs:', err)
    }
  }

  const startTracking = () => {
    flushTimer = setInterval(flushKeystrokes, flushInterval)
  }

  const stopTracking = () => {
    if (flushTimer) { clearInterval(flushTimer); flushTimer = null }
    flushKeystrokes()
  }

  onMounted(startTracking)
  onBeforeUnmount(stopTracking)

  return { logKeystroke, logMouseClick, flushKeystrokes, stopTracking }
}
