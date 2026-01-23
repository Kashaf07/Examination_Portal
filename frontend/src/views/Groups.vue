<template>
  <div class="p-6">
    <h1 class="text-3xl font-bold mb-6">Applicant Groups</h1>

    <!-- CREATE GROUP -->
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
        <button type="submit" class="bg-green-600 text-white px-4 py-2 rounded">
          Create Group
        </button>
      </form>
    </div>

    <!-- GROUP LIST -->
    <div v-if="groups.length" class="bg-white shadow rounded p-4">
      <h2 class="text-xl font-semibold mb-4">Existing Groups</h2>

      <table class="min-w-full border">
        <thead class="bg-gray-100">
          <tr>
            <th class="px-4 py-2">Group Name</th>
            <th class="px-4 py-2">Created By</th>
            <th class="px-4 py-2 text-center">Actions</th>
          </tr>
        </thead>

        <tbody>
          <template v-for="g in groups" :key="g.Group_Id">
            <tr class="border-t">
              <td class="px-4 py-2">{{ g.Group_Name }}</td>
              <td class="px-4 py-2">{{ g.Faculty_Email }}</td>
              <td class="px-4 py-2 text-center">
                <button
                  @click="toggleView(g.Group_Id)"
                  class="bg-blue-500 text-white px-3 py-1 rounded text-xs"
                >
                  {{ expandedGroup === g.Group_Id ? "Hide" : "View" }}
                </button>
              </td>
            </tr>

            <tr v-if="expandedGroup === g.Group_Id">
              <td colspan="3" class="bg-gray-50 p-4">
                <h3 class="font-semibold mb-2">
                  Applicants in {{ g.Group_Name }}
                </h3>

                <table v-if="applicants[g.Group_Id]?.length" class="min-w-full border text-sm">
                  <thead class="bg-gray-200">
                    <tr>
                      <th class="px-2 py-1">Name</th>
                      <th class="px-2 py-1">Email</th>
                      <th class="px-2 py-1">Phone</th>
                      <th class="px-2 py-1">Gender</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="a in applicants[g.Group_Id]"
                      :key="a.Applicant_Id"
                      class="border-t"
                    >
                      <td class="px-2 py-1">{{ a.Full_Name }}</td>
                      <td class="px-2 py-1">{{ a.Email }}</td>
                      <td class="px-2 py-1">{{ a.Phone }}</td>
                      <td class="px-2 py-1">{{ a.Gender }}</td>
                    </tr>
                  </tbody>
                </table>

                <p v-else class="text-gray-500">No applicants in this group</p>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>

    <p v-else class="text-gray-500 text-center">
      No groups created yet
    </p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "../utils/axiosInstance"

// STATE
const groupName = ref("")
const groups = ref([])
const expandedGroup = ref(null)
const applicants = ref({})

// ROLE (FIXED)
const rawRole = (localStorage.getItem("active_role") || "").toLowerCase()
const activeRole = rawRole === "admin" ? "Admin" : "Faculty"

// EMAIL (FIXED)
const email =
  activeRole === "Admin"
    ? localStorage.getItem("admin_email")
    : localStorage.getItem("email")

// LOAD GROUPS
const loadGroups = async () => {
  const res = await axios.get("/groups", {
    params: { role: activeRole, email }
  })
  if (res.data.success) {
    groups.value = res.data.groups
  }
}

// CREATE GROUP
const createGroup = async () => {
  const res = await axios.post("/groups/create", {
    group_name: groupName.value,
    role: activeRole,
    email
  })
  if (res.data.success) {
    groupName.value = ""
    loadGroups()
  }
}

// VIEW APPLICANTS
const toggleView = async (groupId) => {
  expandedGroup.value = expandedGroup.value === groupId ? null : groupId
  if (!applicants.value[groupId]) {
    const res = await axios.get(`/groups/${groupId}/applicants`)
    if (res.data.success) {
      applicants.value[groupId] = res.data.applicants
    }
  }
}

onMounted(loadGroups)
</script>
