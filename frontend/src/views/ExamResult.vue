<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 p-10">
    
    <div class="max-w-6xl mx-auto bg-white rounded-xl shadow-xl p-8">
      
      <h1 class="text-3xl font-bold tracking-tight bg-gradient-to-r from-blue-600 to-purple-700 bg-clip-text text-transparent inline-block">
        Exam {{ examId }} - Final Results
      </h1>

      <div v-if="results.length > 0" class="overflow-x-auto">
        <table class="w-full border">
          <thead class="bg-blue-100">
            <tr>
              <th class="px-4 py-3 text-left">Student ID</th>
              <th class="px-4 py-3 text-left">Email</th>
              <th class="px-4 py-3 text-right">Marks</th>
              <th class="px-4 py-3 text-center">Status</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="r in results" :key="r.Attempt_Id" class="border-t">
              <td class="px-4 py-3">{{ r.Applicant_Id }}</td>
              <td class="px-4 py-3">{{ r.Student_Email }}</td>
              <td class="px-4 py-3 text-right">{{ r.Marks_Obtained }}/{{ r.Max_Marks }}</td>
              <td class="px-4 py-3 text-center">
                <span :class="r.Status === 'Pass' ? 'text-green-600 font-semibold' : 'text-red-500 font-semibold'">
                  {{ r.Status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else class="text-gray-500 italic">
        No results available.
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from '../utils/axiosInstance'

const route = useRoute()
const examId = route.params.examId
const results = ref([])

onMounted(async () => {
  const email = localStorage.getItem("email")
  const role = localStorage.getItem("active_role")

  const res = await axios.get('/attempts', {
    params: { exam_id: examId, email, role }
  })

  if (res.data.success) {
    results.value = res.data.attempts
  }
})
</script>

<style scoped>

.bg-clip-text {
  -webkit-background-clip: text;
  background-clip: text;
}

</style>