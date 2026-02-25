<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 p-10">

    <div class="max-w-6xl mx-auto bg-white rounded-xl shadow-xl p-8">

      <h1 class="text-3xl font-bold tracking-tight bg-gradient-to-r from-blue-600 to-purple-700 bg-clip-text text-transparent inline-block">
        Exam {{ examId }} - Analytics
      </h1>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">

        <div class="bg-blue-100 p-6 rounded-xl text-center">
          <h2 class="text-xl font-bold">Total Attempts</h2>
          <p class="text-3xl font-bold mt-2">{{ total }}</p>
        </div>

        <div class="bg-green-100 p-6 rounded-xl text-center">
          <h2 class="text-xl font-bold">Pass</h2>
          <p class="text-3xl font-bold mt-2">{{ passCount }}</p>
        </div>

        <div class="bg-red-100 p-6 rounded-xl text-center">
          <h2 class="text-xl font-bold">Fail</h2>
          <p class="text-3xl font-bold mt-2">{{ failCount }}</p>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from '../utils/axiosInstance'

const route = useRoute()
const examId = route.params.examId

const attempts = ref([])

const total = computed(() => attempts.value.length)
const passCount = computed(() => attempts.value.filter(a => a.Status === 'Pass').length)
const failCount = computed(() => attempts.value.filter(a => a.Status === 'Fail').length)

onMounted(async () => {
  const email = localStorage.getItem("email")
  const role = localStorage.getItem("active_role")

  const res = await axios.get('/attempts', {
    params: { exam_id: examId, email, role }
  })

  if (res.data.success) {
    attempts.value = res.data.attempts
  }
})
</script>

<style scoped>

.bg-clip-text {
  -webkit-background-clip: text;
  background-clip: text;
}

</style>