<template>
  <div class="p-6 max-w-6xl mx-auto">
    <h2 class="text-3xl font-bold text-blue-700 mb-4">Make Question Paper</h2>
    <p class="text-lg mb-6">Design the question paper for Exam ID: {{ examId }}</p>

    <!-- Available Questions List -->
    <div class="bg-white shadow p-4 rounded mb-6">
      <h3 class="text-xl font-semibold mb-4">Available Questions (Question Bank)</h3>
      <ul>
        <li v-for="q in allQuestions" :key="q.question_id" class="flex justify-between items-center border-b py-2">
          <span>{{ q.question_text }} ({{ q.marks }} marks)</span>
          <button @click="addToPaper(q.question_id)" class="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700">
            Add
          </button>
        </li>
      </ul>
    </div>

    <!-- Selected Questions -->
    <div class="bg-white shadow p-4 rounded mb-6">
      <h3 class="text-xl font-semibold mb-4">Selected Questions (Paper)</h3>
      <div v-if="selectedQuestions.length">
        <ul>
          <li v-for="(q, index) in selectedQuestions" :key="q.question_id" class="flex justify-between items-center border-b py-2">
            <span>{{ index + 1 }}. {{ q.question_text }} ({{ q.marks }} marks)</span>
            <button @click="removeFromPaper(q.question_id)" class="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-700">
              Delete
            </button>
          </li>
        </ul>
        <p class="mt-4 font-semibold">Total Questions: {{ selectedQuestions.length }}</p>
      </div>
      <div v-else class="text-gray-600 italic">No questions added to the paper yet.</div>
    </div>

    <!-- Actions -->
    <div class="flex gap-4">
      <button @click="randomizeQuestions" class="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700">
        Randomize Questions
      </button>
      <button @click="previewPaper" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
        View Paper
      </button>
      <button @click="downloadPDF" class="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700">
        Download PDF
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const examId = route.params.examId

const allQuestions = ref([])
const selectedQuestions = ref([])

// Fetch all available questions from DB
const fetchAllQuestions = async () => {
  try {
    const res = await axios.get(`/api/questionbank/all/${examId}`)
    allQuestions.value = res.data
  } catch (err) {
    console.error('Error loading question bank:', err)
  }
}

// Fetch selected questions for this exam paper
const fetchSelectedQuestions = async () => {
  try {
    const res = await axios.get(`/api/paper/questions/${examId}`)
    selectedQuestions.value = res.data
  } catch (err) {
    console.error('Error loading selected questions:', err)
  }
}

// Add question to paper
const addToPaper = async (questionId) => {
  try {
    await axios.post('/api/paper/add', { exam_id: examId, question_id: questionId })
    fetchSelectedQuestions()
  } catch (err) {
    console.error('Error adding question to paper:', err)
  }
}

// Remove question from paper
const removeFromPaper = async (questionId) => {
  try {
    await axios.delete(`/api/paper/delete/${questionId}`)
    fetchSelectedQuestions()
  } catch (err) {
    console.error('Error removing question:', err)
  }
}

// Randomly select 30 unique questions
const randomizeQuestions = async () => {
  try {
    await axios.post(`/api/paper/randomize/${examId}`)
    fetchSelectedQuestions()
  } catch (err) {
    console.error('Error randomizing questions:', err)
  }
}

// View Paper (e.g., navigate to preview page)
const previewPaper = () => {
  alert("Preview feature coming soon!") // or router.push('/preview')
}

// Download PDF
const downloadPDF = () => {
  window.open(`/api/paper/download/${examId}`, '_blank')
}

onMounted(() => {
  fetchAllQuestions()
  fetchSelectedQuestions()
})
</script>
