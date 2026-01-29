<template>
  <div class="space-y-6">

    <!-- SWITCH BUTTONS -->
    <div class="flex gap-4 mb-4">
      <button
        @click="$router.push('/admin/groups/students')"
        class="px-6 py-3 rounded-full font-semibold shadow-md 
               bg-gray-200 text-gray-700 hover:bg-gray-300 hover:scale-105 transition">
        🎓 Student Groups
      </button>

      <button
        class="px-6 py-3 rounded-full font-semibold shadow-md 
               bg-purple-600 text-white hover:bg-purple-700 hover:scale-105 transition">
        👨‍🏫 Faculty Groups
      </button>
    </div>

    <!-- OUTER WRAPPER (BLUR WHITE CARD) -->
    <div class="bg-white/80 backdrop-blur-sm shadow-xl rounded-2xl p-8 border border-white/20">

      <!-- HEADER -->
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-800 tracking-wide">
          Faculty Groups Management
        </h2>

        <button
          v-if="isAdmin"
          @click="createFacultyGroup"
          class="bg-purple-600 hover:bg-purple-700 text-white font-semibold 
                 px-6 py-3 rounded-full shadow-lg transition hover:scale-105">
          Create Group
        </button>
      </div>

      <!-- INNER CARD -->
      <div class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-200 p-6">

        <!-- CREATE INPUT -->
        <div v-if="isAdmin" class="mb-6 flex gap-3">
          <input
            v-model="groupName"
            placeholder="Enter Faculty Group Name"
            class="w-full max-w-xs px-4 py-3 rounded-xl border bg-purple-50 
                   focus:bg-white focus:ring-2 focus:ring-purple-400 transition"
          />
        </div>

        <!-- GROUP TABLE -->
        <table class="w-full">
          <thead class="bg-gradient-to-r from-purple-50 to-purple-100 text-purple-900">
            <tr>
              <th class="py-3 px-4 font-semibold">Group Name</th>
              <th class="py-3 px-4 text-center font-semibold">Faculty</th>
              <th class="py-3 px-4 text-center font-semibold">Actions</th>
            </tr>
          </thead>

          <tbody class="bg-white divide-y divide-gray-100">
            <template v-for="g in groups" :key="g.Group_Id">

              <!-- GROUP ROW -->
              <tr class="hover:bg-gray-50 transition">
                <td class="px-4 py-4 font-medium text-gray-800">
                  {{ g.Group_Name }}
                </td>

                <td class="px-4 py-4 text-center">
                  <span
                    class="px-3 py-1 rounded-full text-sm font-semibold"
                    :class="facultyCount(g.Group_Id)
                      ? 'bg-green-100 text-green-700'
                      : 'bg-gray-200 text-gray-600'"
                  >
                    👥 {{ facultyCount(g.Group_Id) }}
                  </span>
                </td>

                <td class="px-4 py-4 text-center space-x-2">
                  <button
                    @click="toggleView(g.Group_Id)"
                    class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg 
                           shadow hover:scale-105 transition">
                    {{ expandedGroup === g.Group_Id ? "Hide" : "View" }}
                  </button>

                  <button
                    v-if="isAdmin"
                    @click="toggleAddFaculty(g.Group_Id)"
                    class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg 
                           shadow hover:scale-105 transition">
                    Add Faculty
                  </button>

                  <button
                    v-if="isAdmin"
                    @click="deleteGroup(g.Group_Id)"
                    class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg 
                           shadow hover:scale-105 transition">
                    Delete
                  </button>
                </td>
              </tr>

              <!-- EXPANDED ROW (Below same group) -->
              <tr v-if="expandedGroup === g.Group_Id">
                <td colspan="3" class="bg-gray-50 p-6">

                  <!-- TITLE -->
                  <h3 class="text-lg font-semibold mb-4 text-gray-700">
                    Assigned Faculty for {{ g.Group_Name }}
                  </h3>

                  <!-- ASSIGNED FACULTY TABLE -->
                  <div v-if="facultyMap[g.Group_Id]?.length" class="rounded-2xl shadow-md border bg-white overflow-hidden mb-6">

                    <table class="w-full">
                      <thead class="bg-gradient-to-r from-purple-50 to-purple-100 text-purple-900">
                        <tr>
                          <th class="py-3 px-4 font-semibold text-left">Name</th>
                          <th class="py-3 px-4 font-semibold text-left">Email</th>
                          <th class="py-3 px-4 font-semibold text-center">Action</th>
                        </tr>
                      </thead>

                      <tbody class="bg-white divide-y divide-gray-100">
                        <tr
                          v-for="f in facultyMap[g.Group_Id]"
                          :key="f.Faculty_Id"
                          class="hover:bg-purple-50 transition cursor-pointer"
                        >
                          <td class="px-4 py-3 font-medium text-gray-800">
                            {{ f.Faculty_Name }}
                          </td>

                          <td class="px-4 py-3 text-gray-700">
                            {{ f.Faculty_Email }}
                          </td>

                          <td class="px-4 py-3 text-center">
                            <button
                              v-if="isAdmin"
                              @click="removeFaculty(g.Group_Id, f.Faculty_Id)"
                              class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-full text-sm shadow hover:scale-105 transition"
                            >
                              Remove
                            </button>
                          </td>
                        </tr>
                      </tbody>
                    </table>

                  </div>

                  <!-- EMPTY STATE -->
                  <p v-else class="text-gray-500 italic text-center py-4">
                    No faculty assigned
                  </p>

                  <!-- AVAILABLE FACULTY TABLE -->
                  <div v-if="showAddFaculty === g.Group_Id" class="mt-6 rounded-2xl shadow-md border bg-white overflow-hidden">

                    <table class="w-full">
                      <thead class="bg-gradient-to-r from-blue-50 to-blue-100 text-blue-900">
                        <tr>
                          <th class="py-3 px-4 font-semibold text-left">Name</th>
                          <th class="py-3 px-4 font-semibold text-left">Email</th>
                          <th class="py-3 px-4 font-semibold text-center">Action</th>
                        </tr>
                      </thead>

                      <tbody class="bg-white divide-y divide-gray-100">
                        <tr
                          v-for="f in availableFacultyMap[g.Group_Id]"
                          :key="f.Faculty_Id"
                          class="hover:bg-blue-50 transition cursor-pointer"
                        >
                          <td class="px-4 py-3 font-medium text-gray-800">
                            {{ f.Faculty_Name }}
                          </td>

                          <td class="px-4 py-3 text-gray-700">
                            {{ f.Faculty_Email }}
                          </td>

                          <td class="px-4 py-3 text-center">
                            <button
                              @click="addFaculty(g.Group_Id, f.Faculty_Id)"
                              class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-full text-sm shadow hover:scale-105 transition"
                            >
                              Add
                            </button>
                          </td>
                        </tr>
                      </tbody>
                    </table>

                  </div>
                </td>
              </tr>

            </template>
          </tbody>
        </table>

      </div>
    </div>
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
