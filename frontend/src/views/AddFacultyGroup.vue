<template>
  <div class="bg-white rounded-xl shadow p-6 max-w-lg">
    <h2 class="text-2xl font-bold mb-6 text-gray-800">
      Create Faculty Group
    </h2>

    <form @submit.prevent="createGroup">
      <label class="block mb-2 font-semibold">Group Name</label>
      <input
        v-model="groupName"
        required
        class="w-full border rounded px-3 py-2 mb-4"
        placeholder="Enter group name"
      />

      <div class="flex gap-4">
        <button
          type="submit"
          class="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded"
        >
          Create
        </button>

        <button
          type="button"
          @click="$router.push('/admin/faculty-groups')"
          class="bg-gray-400 hover:bg-gray-500 text-white px-6 py-2 rounded"
        >
          Cancel
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from '@/utils/axiosInstance'
import { useRouter } from 'vue-router'

const router = useRouter()
const groupName = ref('')

const createGroup = async () => {
  await axios.post('/faculty-groups', {
    group_name: groupName.value
  })

  router.push('/admin/faculty-groups')
}
</script>
