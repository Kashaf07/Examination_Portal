<template>
  <div
    class="min-h-screen flex items-center justify-center
           bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50"
  >
    <div
      class="bg-white/80 backdrop-blur-xl shadow-2xl rounded-3xl
             p-12 w-full max-w-3xl border border-white/30"
    >
      <h2 class="text-3xl font-extrabold text-center text-gray-800 mb-14">
        Groups Dashboard
      </h2>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-12">

        <!-- 🎓 STUDENT GROUPS (ADMIN + FACULTY) -->
        <button
          @click="goStudentGroups"
          class="bg-gradient-to-br from-blue-500 to-blue-700
                 text-white py-8 rounded-3xl text-xl font-semibold
                 shadow-xl transition-all duration-300
                 hover:-translate-y-2 hover:shadow-2xl"
        >
          🎓 Student Groups
        </button>

        <!-- 👨‍🏫 FACULTY GROUPS (ADMIN ONLY) -->
        <button
          v-if="isAdmin"
          @click="goFacultyGroups"
          class="bg-gradient-to-br from-purple-500 to-purple-700
                 text-white py-8 rounded-3xl text-xl font-semibold
                 shadow-xl transition-all duration-300
                 hover:-translate-y-2 hover:shadow-2xl"
        >
          👨‍🏫 Faculty Groups
        </button>

      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

/* ================= ROLE (SOURCE OF TRUTH) ================= */
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
