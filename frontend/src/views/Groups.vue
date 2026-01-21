<template>
  <div class="p-6">
    <h1 class="text-3xl font-bold mb-6">Applicant Groups</h1>

    <!-- Create Group -->
    <div class="bg-white shadow rounded p-4 max-w-xl mb-8">
      <h2 class="text-xl font-semibold mb-4">Create Group</h2>
      <form @submit.prevent="createGroup">
        <input
          v-model="groupName"
          type="text"
          placeholder="Group Name"
          class="border p-2 rounded w-full mb-4"
          required
        />
        <button class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
          Create Group
        </button>
      </form>
      <p v-if="message" class="mt-2 text-sm text-blue-600">{{ message }}</p>
    </div>

    <!-- Group List -->
    <div v-if="groups.length" class="bg-white shadow rounded p-4">
      <h2 class="text-xl font-semibold mb-4">Existing Groups</h2>
      <table class="min-w-full border">
        <thead class="bg-gray-100">
          <tr>
            <th class="px-4 py-2">Group Name</th>
            <th class="px-4 py-2 text-center">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="group in groups" :key="group.Group_Id" class="border-t">
            <td class="px-4 py-2">
              <input
                v-if="editId === group.Group_Id"
                v-model="editName"
                class="border p-1 rounded w-full"
              />
              <span v-else>{{ group.Group_Name }}</span>
            </td>
            <td class="px-4 py-2 text-center space-x-2">

              <button
                @click="viewStudents(group.Group_Id)"
                class="bg-blue-500 text-white px-3 py-1 rounded text-xs"
              >
                View Students
              </button>

              <button
                v-if="editId !== group.Group_Id"
                @click="startEdit(group)"
                class="bg-yellow-500 text-white px-3 py-1 rounded text-xs"
              >
                Edit
              </button>

              <button
                v-if="editId === group.Group_Id"
                @click="updateGroup(group.Group_Id)"
                class="bg-green-600 text-white px-3 py-1 rounded text-xs"
              >
                Save
              </button>

              <button
                @click="deleteGroup(group.Group_Id)"
                class="bg-red-500 text-white px-3 py-1 rounded text-xs"
              >
                Delete
              </button>

            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <p v-else class="text-gray-500 text-center">No groups created yet.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from '../utils/axiosInstance'

const router = useRouter()
const facultyEmail = localStorage.getItem('faculty_email')

const groupName = ref('')
const groups = ref([])
const message = ref('')

const editId = ref(null)
const editName = ref('')

const loadGroups = async () => {
  const res = await axios.get(`/groups/${facultyEmail}`)
  if (res.data.success) {
    groups.value = res.data.groups
  }
}

const createGroup = async () => {
  const res = await axios.post('/groups/create', {
    group_name: groupName.value,
    faculty_email: facultyEmail
  })
  if (res.data.success) {
    message.value = 'Group created successfully'
    groupName.value = ''
    loadGroups()
  }
}

const startEdit = (group) => {
  editId.value = group.Group_Id
  editName.value = group.Group_Name
}

const updateGroup = async (groupId) => {
  await axios.put(`/groups/update/${groupId}`, {
    group_name: editName.value
  })
  editId.value = null
  loadGroups()
}

const deleteGroup = async (groupId) => {
  if (!confirm('Delete this group?')) return
  await axios.delete(`/groups/delete/${groupId}`)
  loadGroups()
}

const viewStudents = (groupId) => {
  router.push({ name: 'GroupStudents', params: { groupId } })
}

onMounted(loadGroups)
</script>
