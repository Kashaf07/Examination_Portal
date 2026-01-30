<template>
  <div class="min-h-screen w-full bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 flex flex-col items-center py-10">
    <div class="w-full max-w-[1600px] px-8">
      <!-- Back Button -->
      <button
        @click="goBack"
        class="mb-6 flex items-center gap-2 px-4 py-2 bg-white/70 hover:bg-white/90 
               text-gray-800 rounded-lg shadow-md hover:shadow-lg transition-all duration-200 
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
        <span class="font-semibold">Back</span>
      </button>

      <h1 class="text-3xl font-bold mb-6 text-transparent bg-clip-text bg-gradient-to-r from-purple-700 to-pink-500 tracking-tight">
        Submitted Answers for Attempt {{ attemptId }}
      </h1>
      
      <div v-if="error" class="mb-6 p-4 bg-red-100 text-red-700 border border-red-400 rounded w-full">
        {{ error }}
      </div>
      
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
            <tr v-for="a in answers" :key="a.Answer_Id" class="hover:bg-pink-50 transition-colors duration-150 border-b border-gray-100">
              <td class="py-3 px-6">{{ a.Question_Text }}</td>
              <td class="py-3 px-6 break-words">{{ a.Selected_Option_Id || '-' }}</td>
              <td class="py-3 px-6 break-words">{{ a.Answer_Text || '-' }}</td>
              <td class="py-3 px-6 break-words">{{ a.Correct_Answer || '-' }}</td>
              <td class="py-3 px-6">
                <span :class="isCorrect(a) ? 'text-green-600 font-bold' : 'text-red-600 font-bold'">
                  {{ isCorrect(a) ? 'Correct' : 'Incorrect' }}
                </span>
              </td>
            </tr>
            <tr v-if="answers.length === 0">
              <td colspan="5" class="text-center py-8 text-gray-500 italic">No answers found.</td>
            </tr>
          </tbody>
        </table>
      </div>      
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const attemptId = ref(route.params.attemptId)
const answers = ref([])
const error = ref('')
const examId = ref(null)

const fetchAnswers = async () => {
  error.value = ''
  try {
    const response = await fetch(`http://localhost:5000/api/answers/${attemptId.value}`)
    const data = await response.json()
    if (!response.ok) {
      error.value = data.error || 'Failed to load answers'
    } else {
      answers.value = data.answers
      // Get exam_id from the first answer if available
      if (data.answers && data.answers.length > 0 && data.answers[0].Exam_Id) {
        examId.value = data.answers[0].Exam_Id
      }
    }
  } catch (e) {
    error.value = 'Error fetching answers: ' + e.message
  }
}

const isCorrect = (answer) => {
  if (!answer.Correct_Answer) return false
  return (answer.Answer_Text || '').trim().toLowerCase() === (answer.Correct_Answer || '').trim().toLowerCase()
}

const goBack = () => {
  // Navigate back to ViewResponses for this exam
  const activeRole = localStorage.getItem('active_role')
  
  if (!examId.value) {
    // Fallback: if we don't have exam_id, just go back using browser history
    router.back()
    return
  }
  
  if (activeRole === 'Admin') {
    router.push({ name: 'ViewResponsesAdmin', params: { examId: examId.value } })
  } else if (activeRole === 'Faculty') {
    router.push({ name: 'ViewResponsesFaculty', params: { examId: examId.value } })
  } else {
    router.back()
  }
}

onMounted(fetchAnswers)
</script>

<style scoped>
/* Tailwind handles styling */
</style>