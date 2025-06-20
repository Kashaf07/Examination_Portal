<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h2 class="text-3xl font-bold mb-4 text-blue-700">Make Question Paper</h2>
    <p class="mb-6 text-lg">Feature to design question paper for Exam ID: {{ $route.params.examId }}</p>

    <!-- Add Question Form -->
    <div class="bg-white shadow-md p-4 rounded mb-6">
      <h3 class="text-xl font-semibold mb-3">Add Question</h3>
      <form @submit.prevent="addQuestion">
        <input v-model="newQuestion.text" type="text" placeholder="Question Text" class="border border-gray-300 p-2 rounded mr-2 w-64" required />
        <input v-model.number="newQuestion.marks" type="number" placeholder="Marks" class="border border-gray-300 p-2 rounded mr-2 w-64" required />
        <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Add</button>
      </form>
    </div>

    <!-- Question List -->
    <div v-if="questions.length" class="bg-white shadow-md rounded p-4 mb-4">
      <h3 class="text-xl font-semibold mb-3">Current Questions</h3>
      <ul>
        <li v-for="(q, index) in questions" :key="q.question_id" class="flex justify-between items-center mb-2">
          <span>{{ index + 1 }}. {{ q.question_text }} ({{ q.marks }} marks)</span>
          <button @click="deleteQuestion(q.question_id)" class="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-700">Delete</button>
        </li>
      </ul>
    </div>
    <div v-else class="text-gray-600 italic">No questions added yet.</div>

    <!-- Randomize Button -->
    <div class="mt-6">
      <button @click="randomizeQuestions" class="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700">Randomize Questions</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const route = useRoute()
const examId = route.params.examId
const questions = ref([])
const newQuestion = ref({ text: '', marks: '' })

// Fetch questions
const fetchQuestions = async () => {
  try {
    const res = await axios.get(`/api/question/questions/${examId}`)
    questions.value = res.data
  } catch (err) {
    console.error('Error fetching questions:', err)
  }
}

// Add question
const addQuestion = async () => {
  try {
    await axios.post('/api/question/add', {
      exam_id: examId,
      question_type: 'OneWord', // static for now; later you can make it dynamic
      question_text: newQuestion.value.text,
      correct_answer: 'NA', // or actual answer
      marks: newQuestion.value.marks,
      option_a: null,
      option_b: null,
      option_c: null,
      option_d: null
    })
    newQuestion.value = { text: '', marks: '' }
    fetchQuestions()
  } catch (err) {
    console.error('Error adding question:', err)
  }
}



// Delete question
const deleteQuestion = async (questionId) => {
  try {
    await axios.delete(`/api/question/delete/${questionId}`)
    fetchQuestions()
  } catch (err) {
    console.error('Error deleting question:', err)
  }
}

// Randomize questions
const randomizeQuestions = async () => {
  try {
    await axios.post(`/api/question/randomize/${examId}`)
    fetchQuestions()
  } catch (err) {
    console.error('Error randomizing questions:', err)
  }
}

onMounted(() => {
  fetchQuestions()
})
</script>



