<template>
  <div class="bg-white rounded-xl shadow p-6">
    <h2 class="text-2xl font-bold mb-4">
      Assign Faculty to Group {{ groupId }}
    </h2>

    <div class="mb-4">
      <button
        @click="assignFaculty"
        :disabled="selected.length === 0"
        class="bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white px-5 py-2 rounded"
      >
        Assign Selected ({{ selected.length }})
      </button>
    </div>

    <table class="w-full border">
      <thead class="bg-gray-100">
        <tr>
          <th class="p-3">Select</th>
          <th class="p-3 text-left">Name</th>
          <th class="p-3 text-left">Email</th>
          <th class="p-3 text-center">Status</th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="f in faculty"
          :key="f.Faculty_Id"
          class="border-t"
        >
          <td class="p-3 text-center">
            <input
              type="checkbox"
              :disabled="f.is_assigned"
              :value="f.Faculty_Id"
              v-model="selected"
            />
          </td>

          <td class="p-3">{{ f.Faculty_Name }}</td>
          <td class="p-3">{{ f.Faculty_Email }}</td>

          <td class="p-3 text-center">
            <span
              v-if="f.is_assigned"
              class="text-green-600 font-semibold"
            >
              Assigned ✔
            </span>
            <span v-else class="text-gray-400">
              Not Assigned
            </span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '@/utils/axiosInstance'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const groupId = route.params.groupId

const faculty = ref([])
const selected = ref([])

const fetchFaculty = async () => {
  const res = await axios.get(`/faculty-groups/${groupId}/faculty`)
  faculty.value = res.data.faculty
}

const assignFaculty = async () => {
  await axios.post('/faculty-groups/assign', {
    group_id: groupId,
    faculty_ids: selected.value
  })

  router.push('/admin/faculty-groups')
}

onMounted(fetchFaculty)
</script>
