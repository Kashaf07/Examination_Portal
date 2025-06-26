<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold text-blue-800 mb-6">
      Responses for Exam ID: {{ examId }}
    </h1>

    <div v-if="responses.length">
      <table class="min-w-full bg-white border text-sm">
        <thead class="bg-blue-100 text-blue-800">
          <tr>
            <th class="px-4 py-2">#</th>
            <th class="px-4 py-2">Full Name</th>
            <th class="px-4 py-2">Email</th>
            <th class="px-4 py-2">Status</th>
            <th class="px-4 py-2">Start Time</th>
            <th class="px-4 py-2">End Time</th>
            <th class="px-4 py-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(r, index) in responses" :key="r.Attempt_Id" class="border-t">
            <td class="px-4 py-2">{{ index + 1 }}</td>
            <td class="px-4 py-2">{{ r.Full_Name }}</td>
            <td class="px-4 py-2">{{ r.Email }}</td>
            <td class="px-4 py-2">{{ r.Status }}</td>
            <td class="px-4 py-2">{{ formatDateTime(r.Start_Time) }}</td>
            <td class="px-4 py-2">{{ formatDateTime(r.End_Time) }}</td>
            <td class="px-4 py-2">
              <button class="bg-purple-600 text-white px-3 py-1 rounded text-sm hover:bg-purple-700">
                View Answers
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="text-gray-500 text-center mt-8">
      No responses found for this exam.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const examId = route.params.examId
const responses = ref([])

const fetchResponses = async () => {
  try {
    const res = await axios.get(`http://localhost:5000/api/faculty/view_responses/${examId}`)
    if (res.data.success) {
      responses.value = res.data.responses
    }
  } catch (err) {
    console.error('Failed to fetch responses:', err)
  }
}

const formatDateTime = (datetime) => {
  return new Date(datetime).toLocaleString()
}

onMounted(() => {
  fetchResponses()
})
</script>

<style scoped>
/* Styling like your dashboard */
.p-6 {
  background: linear-gradient(to bottom right, #e0f2fe, #f3e8ff);
  min-height: 100vh;
  font-family: 'Inter', sans-serif;
}
</style>
