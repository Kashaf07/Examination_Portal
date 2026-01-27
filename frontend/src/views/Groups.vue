<template>
  <div class="space-y-6">

    <!-- 🔁 GROUP SWITCH (ADMIN ONLY) -->
    <div v-if="isAdmin" class="flex gap-4 mb-4">

      <!-- STUDENT GROUPS -->
      <button
        class="px-6 py-2 rounded-full font-semibold
               bg-blue-600 text-white shadow"
      >
        🎓 Student Groups
      </button>

      <!-- FACULTY GROUPS -->
      <button
        @click="$router.push('/admin/groups/faculty')"
        class="px-6 py-2 rounded-full font-semibold
               bg-gray-200 text-gray-700 hover:bg-gray-300"
      >
        👨‍🏫 Faculty Groups
      </button>

    </div>

    <!-- MAIN CARD -->
    <div class="bg-white shadow-xl rounded-2xl p-8">

      <!-- HEADER -->
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-800">
          Applicant Groups
        </h2>

        <button
          @click="createGroup"
          class="bg-blue-600 hover:bg-blue-700
                 text-white px-6 py-2 rounded-full font-semibold"
        >
          Create Group
        </button>
      </div>

      <!-- CREATE GROUP INPUT -->
      <input
        v-model="groupName"
        placeholder="Enter Group Name"
        class="mb-6 w-full max-w-sm px-4 py-2 border rounded-xl"
      />

      <!-- GROUPS TABLE -->
      <table class="w-full border rounded-xl overflow-hidden">
        <thead class="bg-gray-100">
          <tr>
            <th class="p-3 text-left">Group</th>
            <th class="p-3 text-center">Applicants</th>
            <th class="p-3 text-center">Actions</th>
          </tr>
        </thead>

        <tbody>
          <template v-for="g in groups" :key="g.Group_Id">

            <!-- GROUP ROW -->
            <tr class="border-t">
              <td class="p-3 font-medium">
                {{ g.Group_Name }}
              </td>

              <!-- COUNT -->
              <td class="p-3 text-center">
                <span
                  class="inline-flex items-center gap-1 px-3 py-1
                         rounded-full text-sm font-semibold"
                  :class="(applicants[g.Group_Id]?.length || 0) > 0
                    ? 'bg-green-100 text-green-700'
                    : 'bg-gray-200 text-gray-600'"
                >
                  👥 {{ applicants[g.Group_Id]?.length || 0 }}
                </span>
              </td>

              <td class="p-3 text-center space-x-2">
                <button
                  @click="toggleView(g.Group_Id)"
                  class="bg-blue-600 text-white px-4 py-1 rounded"
                >
                  {{ expandedGroup === g.Group_Id ? 'Hide' : 'View' }}
                </button>

                <button
                  @click="deleteGroup(g.Group_Id)"
                  class="bg-red-600 hover:bg-red-700
                         text-white px-4 py-1 rounded"
                >
                  Delete
                </button>
              </td>
            </tr>

            <!-- EXPANDED APPLICANTS -->
            <tr v-if="expandedGroup === g.Group_Id">
              <td colspan="3" class="bg-gray-50 p-4">

                <h3 class="font-semibold mb-3">
                  Applicants in {{ g.Group_Name }}
                </h3>

                <table
                  v-if="applicants[g.Group_Id]?.length"
                  class="w-full border rounded-lg"
                >
                  <thead class="bg-gray-200">
                    <tr>
                      <th class="p-2 text-left">Name</th>
                      <th class="p-2 text-left">Email</th>
                      <th class="p-2 text-center">Action</th>
                    </tr>
                  </thead>

                  <tbody>
                    <tr
                      v-for="a in applicants[g.Group_Id]"
                      :key="a.Applicant_Id"
                      class="border-t"
                    >
                      <td class="p-2">{{ a.Full_Name }}</td>
                      <td class="p-2">{{ a.Email }}</td>
                      <td class="p-2 text-center">
                        <button
                          @click="removeApplicant(g.Group_Id, a.Applicant_Id)"
                          class="bg-red-600 hover:bg-red-700
                                 text-white px-2 py-1 rounded"
                        >
                          Remove
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>

                <p v-else class="italic text-gray-500">
                  No applicants in this group
                </p>

              </td>
            </tr>

          </template>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import axios from "@/utils/axiosInstance"

const groupName = ref("")
const groups = ref([])
const applicants = ref({})
const expandedGroup = ref(null)

/* 🔐 ROLE */
const role =
  (localStorage.getItem("active_role") || "").toLowerCase() === "admin"
    ? "Admin"
    : "Faculty"

/* ✅ ADMIN CHECK */
const isAdmin = computed(() => role === "Admin")

const email = localStorage.getItem("email")

/* LOAD GROUPS + COUNTS */
const loadGroups = async () => {
  const res = await axios.get("/groups", {
    params: { role, email }
  })

  if (res.data.success) {
    groups.value = res.data.groups
    preloadApplicantCounts()
  }
}

/* PRELOAD COUNTS */
const preloadApplicantCounts = async () => {
  for (const g of groups.value) {
    const res = await axios.get(`/groups/${g.Group_Id}/applicants`)
    applicants.value[g.Group_Id] = res.data.success
      ? res.data.applicants
      : []
  }
}

/* CREATE GROUP */
const createGroup = async () => {
  if (!groupName.value.trim()) return

  await axios.post("/groups/create", {
    group_name: groupName.value,
    role,
    email
  })

  groupName.value = ""
  loadGroups()
}

/* TOGGLE VIEW */
const toggleView = (groupId) => {
  expandedGroup.value =
    expandedGroup.value === groupId ? null : groupId
}

/* REMOVE APPLICANT */
const removeApplicant = async (groupId, applicantId) => {
  if (!confirm("Remove applicant from this group?")) return

  await axios.post("/groups/remove-applicant", {
    group_id: groupId,
    applicant_id: applicantId
  })

  applicants.value[groupId] =
    applicants.value[groupId].filter(
      a => a.Applicant_Id !== applicantId
    )
}

/* DELETE GROUP */
const deleteGroup = async (groupId) => {
  if (!confirm("Delete this group permanently?")) return

  await axios.delete(`/groups/${groupId}`)
  expandedGroup.value = null
  loadGroups()
}

onMounted(loadGroups)
</script>
