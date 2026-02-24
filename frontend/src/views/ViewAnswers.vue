<template>
  <!-- ================= AUTHORIZED CONTENT ================= -->
  <div
    v-if="!error"
    class="min-h-screen w-full bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 flex flex-col items-center py-10"
  >
    <div class="w-full max-w-[1600px] px-8">

      <!-- Back Button -->
      <button
        @click="goBack"
        class="mb-6 flex items-center gap-2 px-4 py-2 bg-white/70 hover:bg-white/90 
               text-gray-800 rounded-lg shadow-md hover:shadow-lg transition-all duration-200 
               backdrop-blur-sm border border-gray-200"
      >
        ← Back
      </button>

      <h1 class="text-3xl font-bold mb-6 text-transparent bg-clip-text bg-gradient-to-r from-purple-700 to-pink-500 tracking-tight">
        Submitted Answers for Attempt {{ attemptId }}
      </h1>

      <div class="rounded-xl shadow-xl overflow-x-auto bg-white">
        <table class="min-w-full border-separate border-spacing-0">
          <thead>
            <tr class="bg-gradient-to-r from-purple-200 to-pink-200 text-purple-900 font-bold">
              <th class="py-4 px-6 text-left">Question</th>
              <th class="py-4 px-6 text-left">Selected Option</th>
              <th class="py-4 px-6 text-left">Answer Text</th>
              <th class="py-4 px-6 text-left">Correct Answer</th>
              <th class="py-4 px-6 text-left">Result</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="a in answers" :key="a.Answer_Id" class="hover:bg-pink-50 border-b border-gray-100">
              <td class="py-3 px-6">{{ a.Question_Text }}</td>
              <td class="py-3 px-6">{{ a.Selected_Option_Id || '-' }}</td>
              <td class="py-3 px-6">{{ a.Answer_Text || '-' }}</td>
              <td class="py-3 px-6">{{ a.Correct_Answer || '-' }}</td>
              <td class="py-3 px-6">
                <span :class="isCorrect(a) ? 'text-green-600 font-bold' : 'text-red-600 font-bold'">
                  {{ isCorrect(a) ? 'Correct' : 'Incorrect' }}
                </span>
              </td>
            </tr>
            <tr v-if="answers.length === 0">
              <td colspan="5" class="text-center py-8 text-gray-500 italic">
                No answers found.
              </td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
  </div>

  <!-- ================= ERROR / UNAUTHORIZED SCREEN ================= -->
  <div
    v-else
    class="min-h-screen flex items-center justify-center 
           bg-gradient-to-br from-red-50 via-pink-50 to-orange-50"
  >
    <div class="bg-white shadow-2xl rounded-2xl p-10 text-center max-w-md w-full">

      <div class="text-5xl mb-4">⚠️</div>

      <h2 class="text-3xl font-bold text-red-600 mb-4">
        {{ errorTitle }}
      </h2>

      <p class="text-gray-600 mb-6">
        {{ error }}
      </p>

      <button
        @click="goBack"
        class="bg-gradient-to-r from-red-500 to-pink-500 
               hover:from-pink-600 hover:to-red-600 
               text-white font-semibold px-6 py-3 rounded-full 
               shadow-lg transition-all hover:scale-105"
      >
        Go Back
      </button>

    </div>
  </div>
</template>
<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from '../utils/axiosInstance'

const route = useRoute()
const router = useRouter()

const attemptId = ref(route.params.attemptId)
const answers = ref([])
const error = ref('')
const errorTitle = ref('')

const fetchAnswers = async () => {
  error.value = ''
  answers.value = []

  try {
    const email = localStorage.getItem("email")
    const role = localStorage.getItem("active_role")

    const res = await axios.get(`/answers/${attemptId.value}`, {
      params: { email, role }
    })

    if (res.data.success === false) {
      throw { response: { status: 403 } }
    }

    answers.value = res.data.answers || []

  } catch (err) {
    if (err.response?.status === 403) {
      errorTitle.value = "403 - Unauthorized"
      error.value = "You are not allowed to view this attempt."
    }
    else if (err.response?.status === 404) {
      errorTitle.value = "404 - Not Found"
      error.value = "Attempt not found."
    }
    else {
      errorTitle.value = "Error"
      error.value = "Something went wrong while loading answers."
    }
  }
}
const isCorrect = (answer) => {
  if (!answer.Correct_Answer) return false
  return (answer.Answer_Text || '').trim().toLowerCase() === 
         (answer.Correct_Answer || '').trim().toLowerCase()
}

const goBack = () => {
  router.back()
}

onMounted(fetchAnswers)
</script>

<style scoped>
/* Tailwind handles styling */
</style>