<template>
  <div
    v-if="isOpen"
    @click.self="closeModal"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[9999] p-4"
  >
    <div
      class="bg-white rounded-2xl shadow-2xl max-w-md w-full p-8 relative transform transition-all"
      @click.stop
    >
      <!-- Close Button -->
      <button
        @click="closeModal"
        class="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <!-- Title - Exam Name as Main Heading -->
      <h2 class="text-2xl font-bold text-gray-800 mb-6 text-center">
        {{ examName }}
      </h2>

      <!-- QR Code Container -->
      <div class="flex justify-center mb-6 bg-gradient-to-br from-blue-50 to-indigo-50 p-6 rounded-xl">
        <div
          ref="qrContainer"
          class="bg-white p-4 rounded-lg shadow-lg"
        ></div>
      </div>

      <!-- Exam Link Display -->
      <div class="mb-6">
        <label class="block text-sm font-semibold text-gray-700 mb-2">
          Exam Link:
        </label>
        <div class="flex items-center gap-2">
          <input
            :value="examLink"
            readonly
            class="flex-1 px-4 py-2 bg-gray-50 border border-gray-300 rounded-lg text-sm text-gray-600 focus:outline-none"
          />
          <button
            @click="copyLink"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition text-sm font-semibold"
          >
            📋 Copy
          </button>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex gap-3">
        <button
          @click="copyQRCode"
          class="flex-1 bg-gradient-to-r from-green-500 to-green-600 text-white px-4 py-3 rounded-xl font-semibold hover:from-green-600 hover:to-green-700 transition shadow-md hover:shadow-lg"
        >
          📋 Copy QR Code
        </button>
        <button
          @click="downloadQRCode"
          class="flex-1 bg-gradient-to-r from-blue-500 to-blue-600 text-white px-4 py-3 rounded-xl font-semibold hover:from-blue-600 hover:to-blue-700 transition shadow-md hover:shadow-lg"
        >
          💾 Download
        </button>
      </div>

      <!-- Success Message -->
      <div
        v-if="successMessage"
        class="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm text-center font-medium"
      >
        {{ successMessage }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  examId: {
    type: [String, Number],
    required: true
  },
  examName: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['close'])

const qrContainer = ref(null)
const successMessage = ref('')
const qrCodeInstance = ref(null)

// Automatically detect the base URL (localhost or production)
const baseUrl = window.location.origin
const examLink = ref(`${baseUrl}/student?examId=${props.examId}`)

// Load QRCode.js from CDN
const loadQRCodeLibrary = () => {
  return new Promise((resolve, reject) => {
    if (window.QRCode) {
      resolve()
      return
    }

    const script = document.createElement('script')
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js'
    script.onload = resolve
    script.onerror = reject
    document.head.appendChild(script)
  })
}

// Generate QR Code
const generateQRCode = async () => {
  try {
    await loadQRCodeLibrary()
    
    if (qrContainer.value) {
      // Clear previous QR code
      qrContainer.value.innerHTML = ''
      
      // Generate new QR code
      qrCodeInstance.value = new window.QRCode(qrContainer.value, {
        text: examLink.value,
        width: 256,
        height: 256,
        colorDark: '#1e40af',
        colorLight: '#ffffff',
        correctLevel: window.QRCode.CorrectLevel.H
      })
    }
  } catch (error) {
    console.error('Failed to generate QR code:', error)
  }
}

// Copy Link to Clipboard
const copyLink = async () => {
  try {
    await navigator.clipboard.writeText(examLink.value)
    showSuccess('Link copied to clipboard!')
  } catch (error) {
    console.error('Failed to copy link:', error)
    showSuccess('Failed to copy link')
  }
}

// Copy QR Code as Image
const copyQRCode = async () => {
  try {
    const canvas = qrContainer.value?.querySelector('canvas')
    if (!canvas) {
      showSuccess('QR code not ready')
      return
    }

    // Convert canvas to blob
    canvas.toBlob(async (blob) => {
      try {
        await navigator.clipboard.write([
          new ClipboardItem({ 'image/png': blob })
        ])
        showSuccess('QR code copied to clipboard!')
      } catch (error) {
        console.error('Clipboard API failed, falling back to download:', error)
        downloadQRCode()
        showSuccess('Browser does not support copying images. Downloaded instead!')
      }
    })
  } catch (error) {
    console.error('Failed to copy QR code:', error)
    showSuccess('Failed to copy QR code')
  }
}

// Download QR Code as PNG
const downloadQRCode = () => {
  try {
    const canvas = qrContainer.value?.querySelector('canvas')
    if (!canvas) {
      showSuccess('QR code not ready')
      return
    }

    const url = canvas.toDataURL('image/png')
    const link = document.createElement('a')
    // Replace spaces and special characters with underscores for clean filename
    const cleanExamName = props.examName.replace(/[^a-zA-Z0-9]/g, '_')
    link.download = `${cleanExamName}_QR.png`
    link.href = url
    link.click()
    
    showSuccess('QR code downloaded!')
  } catch (error) {
    console.error('Failed to download QR code:', error)
    showSuccess('Failed to download QR code')
  }
}

// Show Success Message
const showSuccess = (message) => {
  successMessage.value = message
  setTimeout(() => {
    successMessage.value = ''
  }, 3000)
}

// Close Modal
const closeModal = () => {
  emit('close')
}

// Watch for modal open and generate QR code
watch(() => props.isOpen, async (newValue) => {
  if (newValue) {
    await nextTick()
    generateQRCode()
  }
})
</script>

<style scoped>
/* Ensure modal appears above everything */
.z-\[9999\] {
  z-index: 9999;
}
</style>