<template>
  <!-- 🔁 GROUP SWITCH -->
    <div class="flex gap-4 mb-4">
      <button
        @click="$router.push('/admin/groups/students')"
        class="px-6 py-2 rounded-full font-semibold transition
               bg-gray-200 text-gray-700 hover:bg-gray-300"
      >
        🎓 Student Groups
      </button>

      <button
        class="px-6 py-2 rounded-full font-semibold transition
               bg-purple-600 text-white shadow"
      >
        👨‍🏫 Faculty Groups
      </button>
    </div>

  <div class="bg-white rounded-xl shadow p-6 space-y-6">

    
    <h2 class="text-2xl font-bold text-gray-800">Faculty Groups</h2>

    <!-- CREATE GROUP -->
    <div v-if="isAdmin" class="flex items-center gap-4">
      <input
        v-model="groupName"
        type="text"
        placeholder="Enter Faculty Group Name"
        class="px-4 py-2 border rounded-lg w-full max-w-sm"
      />
      <button
        @click="createFacultyGroup"
        class="bg-purple-600 text-white px-6 py-2 rounded-lg"
      >
        Create Group
      </button>
    </div>

    <table class="w-full border">
      <thead class="bg-gray-100">
        <tr>
          <th class="p-3">ID</th>
          <th class="p-3">Name</th>
          <th class="p-3 text-center">Faculty</th>
          <th class="p-3 text-center">Actions</th>
        </tr>
      </thead>

      <tbody>
        <template v-for="g in groups" :key="g.Group_Id">

          <tr class="border-t">
            <td class="p-3">{{ g.Group_Id }}</td>
            <td class="p-3">{{ g.Group_Name }}</td>

            <!-- COUNT -->
            <td class="p-3 text-center">
              <span
                class="inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-semibold"
                :class="facultyCount(g.Group_Id) > 0
                  ? 'bg-green-100 text-green-700'
                  : 'bg-gray-200 text-gray-600'"
              >
                👥 {{ facultyCount(g.Group_Id) }}
              </span>
            </td>

            <td class="p-3 text-center space-x-2">
              <button
                @click="toggleView(g.Group_Id)"
                class="bg-blue-600 text-white px-3 py-1 rounded"
              >
                {{ expandedGroup === g.Group_Id ? 'Hide' : 'View' }}
              </button>

              <button
                v-if="isAdmin"
                @click="toggleAddFaculty(g.Group_Id)"
                class="bg-green-600 text-white px-3 py-1 rounded"
              >
                Add Faculty
              </button>

              <button
                v-if="isAdmin"
                @click="deleteGroup(g.Group_Id)"
                class="bg-red-600 text-white px-3 py-1 rounded"
              >
                Delete
              </button>
            </td>
          </tr>

          <!-- EXPANDED -->
          <tr v-if="expandedGroup === g.Group_Id">
            <td colspan="4" class="bg-gray-50 p-4">

              <h3 class="font-semibold mb-2">Assigned Faculty</h3>

              <table
                v-if="facultyMap[g.Group_Id]?.length"
                class="w-full border mb-4"
              >
                <tr v-for="f in facultyMap[g.Group_Id]" :key="f.Faculty_Id">
                  <td class="p-2">{{ f.Faculty_Name }}</td>
                  <td class="p-2">{{ f.Faculty_Email }}</td>
                  <td class="p-2 text-center">
                    <button
                      v-if="isAdmin"
                      @click="removeFaculty(g.Group_Id, f.Faculty_Id)"
                      class="bg-red-500 text-white px-2 py-1 rounded"
                    >
                      Remove
                    </button>
                  </td>
                </tr>
              </table>

              <p v-else class="italic text-gray-500">
                No faculty assigned
              </p>

              <!-- ADD FACULTY -->
              <div v-if="showAddFaculty === g.Group_Id">
                <h4 class="font-semibold mb-2">Available Faculty</h4>

                <table class="w-full border">
                  <tr
                    v-for="f in availableFacultyMap[g.Group_Id]"
                    :key="f.Faculty_Id"
                  >
                    <td class="p-2">{{ f.Faculty_Name }}</td>
                    <td class="p-2">{{ f.Faculty_Email }}</td>
                    <td class="p-2 text-center">
                      <button
                        @click="addFaculty(g.Group_Id, f.Faculty_Id)"
                        class="bg-blue-600 text-white px-2 py-1 rounded"
                      >
                        Add
                      </button>
                    </td>
                  </tr>
                </table>
              </div>

            </td>
          </tr>

        </template>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from '@/utils/axiosInstance'

const groups = ref([])
const groupName = ref('')
const expandedGroup = ref(null)
const facultyMap = ref({})
const availableFacultyMap = ref({})
const showAddFaculty = ref(null)

const isAdmin = computed(() =>
  localStorage.getItem('active_role') === 'Admin'
)

/* 🔢 FACULTY COUNT */
const facultyCount = (groupId) => {
  return facultyMap.value[groupId]?.length || 0
}

/* FETCH GROUPS */
const fetchGroups = async () => {
  const res = await axios.get('/faculty-groups')
  groups.value = res.data.groups || []

  // 🔥 PRELOAD FACULTY COUNTS
  await preloadFacultyCounts()
}

/* 🔥 PRELOAD COUNTS WITHOUT CLICKING VIEW */
const preloadFacultyCounts = async () => {
  for (const g of groups.value) {
    try {
      const res = await axios.get(`/faculty-groups/${g.Group_Id}/faculty`)
      facultyMap.value[g.Group_Id] = res.data.faculty || []
    } catch (err) {
      facultyMap.value[g.Group_Id] = []
    }
  }
}

/* CREATE GROUP */
const createFacultyGroup = async () => {
  if (!groupName.value.trim()) return alert('Group name required')

  await axios.post('/faculty-groups/create', {
    group_name: groupName.value,
    role: 'Admin'
  })

  groupName.value = ''
  fetchGroups()
}

/* TOGGLE VIEW */
const toggleView = async (groupId) => {
  expandedGroup.value =
    expandedGroup.value === groupId ? null : groupId

  showAddFaculty.value = null
}

/* TOGGLE ADD FACULTY */
const toggleAddFaculty = async (groupId) => {
  expandedGroup.value = groupId
  showAddFaculty.value =
    showAddFaculty.value === groupId ? null : groupId

  if (!availableFacultyMap.value[groupId]) {
    const res = await axios.get(
      `/faculty-groups/${groupId}/available-faculty`
    )
    availableFacultyMap.value[groupId] = res.data.faculty || []
  }
}

/* ADD FACULTY */
const addFaculty = async (groupId, facultyId) => {
  await axios.post('/faculty-groups/add-faculty', {
    group_id: groupId,
    faculty_id: facultyId
  })

  const assigned = await axios.get(`/faculty-groups/${groupId}/faculty`)
  const available = await axios.get(
    `/faculty-groups/${groupId}/available-faculty`
  )

  facultyMap.value[groupId] = assigned.data.faculty
  availableFacultyMap.value[groupId] = available.data.faculty
}

/* REMOVE FACULTY */
const removeFaculty = async (groupId, facultyId) => {
  if (!confirm('Remove faculty from this group?')) return

  await axios.post('/faculty-groups/remove-faculty', {
    group_id: groupId,
    faculty_id: facultyId
  })

  facultyMap.value[groupId] =
    facultyMap.value[groupId].filter(f => f.Faculty_Id !== facultyId)
}

/* DELETE GROUP */
const deleteGroup = async (groupId) => {
  if (!confirm('Delete this faculty group?')) return

  await axios.delete(`/faculty-groups/${groupId}`)
  fetchGroups()
  expandedGroup.value = null
  showAddFaculty.value = null
}

onMounted(fetchGroups)
</script>
