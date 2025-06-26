<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-100 to-pink-100 px-6 py-6">
    <!-- Header with Welcome & Logout -->
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bold text-blue-900">
        Welcome, {{ adminName }}
      </h1>
      <button
        class="logout-btn"
        @click="logout"
      >
        Logout
      </button>
    </div>

    <!-- Actions Section -->
    <div class="flex flex-wrap gap-4 mb-6">
      <button class="bg-blue-600 text-white font-semibold px-6 py-2 rounded-xl shadow-md transition transform hover:scale-105 hover:shadow-lg">
        Manage Users
      </button>
      <button class="bg-blue-600 text-white font-semibold px-6 py-2 rounded-xl shadow-md transition transform hover:scale-105 hover:shadow-lg">
        View Login Logs
      </button>
      <button class="bg-blue-600 text-white font-semibold px-6 py-2 rounded-xl shadow-md transition transform hover:scale-105 hover:shadow-lg">
        Create Exam
      </button>
    </div>

    <!-- Placeholder for future admin content -->
    <div class="bg-white p-6 rounded-xl shadow-md">
      <p class="text-gray-700 text-lg">
        This is the Admin Dashboard. Choose an action to manage the portal.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const adminName = ref('Admin')
const router = useRouter()

onMounted(() => {
  const name = localStorage.getItem('faculty_name') // Reuse same key if you're not storing separately for admin
  if (name) adminName.value = name
})

const logout = async () => {
  const email = localStorage.getItem('faculty_email') // Again, adjust if you use different keys for admin
  const role = 'Admin'

  try {
    await axios.post('http://localhost:5000/api/auth/logout', {
      email,
      role
    })

    localStorage.removeItem('faculty_email')
    localStorage.removeItem('faculty_name')
    router.push('/')
  } catch (err) {
    console.error('Logout error:', err)
    alert('Logout failed. Try again.')
  }
}
</script>

<style scoped>
.logout-btn {
  background: linear-gradient(to right, #ef4444, #b51a1a);
  padding: 0.5rem 1.25rem;
  border-radius: 1rem;
  font-weight: 600;
  color: white;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
}

.logout-btn:hover {
  background: linear-gradient(to right, #c02323, #991b1b);
  transform: scale(1.03);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
}
</style>
