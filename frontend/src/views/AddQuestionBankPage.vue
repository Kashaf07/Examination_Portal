<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold mb-4">Add Question Bank</h2>
    <p>Feature to add questions for Exam ID: {{ $route.params.examId }}</p>
    <!-- Implement your logic here -->
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()
</script>
