<template>
  <div class="space-y-6">
    <div class="flex gap-4 mb-4">
      <!-- 🎓 STUDENT GROUPS (ADMIN + FACULTY) -->
      <button
        @click="goStudentGroups"
        class="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all hover:scale-105">          
        🎓 Student Groups
      </button>

        <!-- 👨‍🏫 FACULTY GROUPS (ADMIN ONLY) -->
        <button
          v-if="isAdmin"
          @click="goFacultyGroups"
          class="bg-purple-500 hover:bg-purple-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all hover:scale-105">
          👨‍🏫 Faculty Groups
        </button>
      </div>
      <!-- MAIN DASHBOARD CARD -->
      <div
        class="bg-white shadow-xl rounded-2xl p-10 border border-gray-200 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
        <h2 class="text-2xl font-extrabold text-gray-800 mb-4">
          Groups Dashboard
        </h2>
        <p class="text-gray-700 text-lg leading-relaxed">
          Select a group category above to manage student or faculty groups.
        </p>
      </div>    
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

/* ================= ROLE ================= */
const activeRole = computed(() => {
  return localStorage.getItem('active_role')
})

const isAdmin = computed(() => activeRole.value === 'Admin')

/* ================= NAVIGATION ================= */

/**
 * Admin   → /admin/groups/students
 * Faculty → /faculty/groups
 */
const goStudentGroups = () => {
  if (activeRole.value === 'Admin') {
    router.push('/admin/groups/students')
    return
  }

  if (activeRole.value === 'Faculty') {
    router.push('/faculty/groups')
    return
  }

  // Safety fallback
  router.push('/')
}

/**
 * Admin only
 */
const goFacultyGroups = () => {
  if (isAdmin.value) {
    router.push('/admin/groups/faculty')
  }
}
</script>
