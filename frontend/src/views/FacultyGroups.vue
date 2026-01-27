<template>
  <div class="bg-white rounded-xl shadow p-6">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-800">Faculty Groups</h2>

      <button
        @click="$router.push('/admin/faculty-groups/add')"
        class="bg-purple-600 hover:bg-purple-700 text-white px-5 py-2 rounded-lg font-semibold"
      >
        + Add Faculty Group
      </button>
    </div>

    <table class="w-full border">
      <thead class="bg-gray-100">
        <tr>
          <th class="p-3 text-left">Group ID</th>
          <th class="p-3 text-left">Group Name</th>
          <th class="p-3 text-center">Actions</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="g in groups" :key="g.Group_Id" class="border-t">
          <td class="p-3">{{ g.Group_Id }}</td>
          <td class="p-3 font-medium">{{ g.Group_Name }}</td>
          <td class="p-3 text-center">
            <button
              @click="goToAddFaculty(g.Group_Id)"
              class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-1 rounded"
            >
              Add Faculty
            </button>
          </td>
        </tr>

        <tr v-if="groups.length === 0">
          <td colspan="3" class="p-6 text-center text-gray-500">
            No faculty groups found
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '@/utils/axiosInstance'
import { useRouter } from 'vue-router'

const router = useRouter()
const groups = ref([])

const fetchGroups = async () => {
  const res = await axios.get('/faculty-groups')
  groups.value = res.data.groups || []
}

const goToAddFaculty = (groupId) => {
  router.push(`/admin/faculty-groups/${groupId}/add-faculty`)
}

onMounted(fetchGroups)
</script>
