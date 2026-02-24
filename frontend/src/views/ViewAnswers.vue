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
  class="mb-6 flex items-center gap-2 px-5 py-3 
         bg-white/70 hover:bg-white/90 
         text-gray-800 rounded-xl 
         shadow-lg hover:shadow-xl 
         transition-all duration-200 
         backdrop-blur-sm border border-gray-200"
>
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    class="h-5 w-5" 
    viewBox="0 0 20 20" 
    fill="currentColor"
  >
    <path 
      fill-rule="evenodd" 
      d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" 
      clip-rule="evenodd" 
    />
  </svg>

  <span class="font-semibold text-lg">Back</span>
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

<!-- UNAUTHORIZED UI -->
<div
  v-else
  class="min-h-screen flex items-center justify-center bg-red-50"
>
  <div class="bg-white shadow-xl rounded-xl p-8 text-center w-full max-w-md">
    
    <h2 class="text-2xl font-bold text-red-600 mb-4">
      Unauthorized Access
    </h2>

    <p class="text-gray-600 mb-6">
      You are not allowed to access this exam.
    </p>

    <!-- Go Back Button -->
    <button
      @click="router.back()"
      class="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-lg font-semibold shadow-md transition"
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