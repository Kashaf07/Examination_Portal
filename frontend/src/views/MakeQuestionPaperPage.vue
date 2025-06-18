<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold mb-4">Make Question Paper</h2>
    <p>Feature to design question paper for Exam ID: {{ $route.params.examId }}</p>
    <!-- Implement your logic here -->
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()
</script>
