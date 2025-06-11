<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-600 via-pink-500 to-red-400 px-4">
    <div class="bg-white rounded-2xl shadow-xl p-8 w-full max-w-md">
      <h2 class="text-3xl font-bold text-center text-gray-800 mb-6">Examination Portal</h2>

      <div class="space-y-5">
        <div>
          <label class="text-sm font-semibold text-gray-700 block mb-1">Email</label>
          <input
            v-model="email"
            type="email"
            placeholder="you@example.com"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
        </div>

        <div>
          <label class="text-sm font-semibold text-gray-700 block mb-1">Password</label>
          <input
            v-model="password"
            type="password"
            placeholder="••••••••"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
        </div>

        <div>
          <label class="text-sm font-semibold text-gray-700 block mb-1">Select Role</label>
          <select
            v-model="role"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          >
            <option>Admin</option>
            <option>Faculty</option>
            <option>Student</option>
          </select>
        </div>

        <button
          @click="login"
          class="w-full bg-purple-600 hover:bg-purple-700 text-white py-2 rounded-lg font-semibold transition"
        >
          Login
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const role = ref('Admin')
const router = useRouter()

const login = async () => {
  try {
    const res = await axios.post('http://localhost:5000/api/auth/login', {
      email: email.value,
      password: password.value,
      role: role.value
    })

    if (res.data.status === 'success') {
      router.push(`/${role.value.toLowerCase()}`)
    } else {
      alert('Invalid credentials')
    }
  } catch (err) {
    alert('Server error')
    console.error(err)
  }
}
</script>
