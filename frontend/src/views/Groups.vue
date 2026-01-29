<template>
  <div class="space-y-6">

    <!-- Top Switch Buttons -->
    <div v-if="isAdmin" class="flex gap-4 mb-4">
      <button
        class="px-6 py-3 rounded-full font-semibold shadow-md bg-blue-600 text-white 
               hover:bg-blue-700 hover:scale-105 transition">
        🎓 Student Groups
      </button>

      <button
        @click="$router.push('/admin/groups/faculty')"
        class="px-6 py-3 rounded-full font-semibold shadow-md bg-gray-200 text-gray-700 
               hover:bg-gray-300 hover:scale-105 transition">
        👨‍🏫 Faculty Groups
      </button>
    </div>

    <!-- OUTER WRAPPER CARD (LIKE SCHOOLS PAGE) -->
    <div class="bg-white/80 backdrop-blur-sm shadow-xl rounded-2xl p-8 border border-white/20">

      <!-- HEADER -->
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-800 tracking-wide">
          Student Groups Management
        </h2>

        <button
          @click="createGroup"
          class="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6 py-3 
                 rounded-full shadow-lg transition hover:scale-105">
          Create Group
        </button>
      </div>

      <!-- INNER CARD (LIKE TABLE WRAPPER) -->
      <div class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-200 p-6">

        <!-- CREATE INPUT -->
        <div class="mb-6 flex gap-3">
          <input
            v-model="groupName"
            placeholder="Enter Group Name"
            class="w-full max-w-xs px-4 py-3 rounded-xl border bg-purple-50 focus:bg-white 
                   focus:ring-2 focus:ring-blue-400 transition"
          />
        </div>

        <!-- GROUPS TABLE -->
        <table class="w-full">
          <thead class="bg-gradient-to-r from-blue-50 to-blue-100 text-blue-900">
            <tr>
              <th class="py-3 px-4 font-semibold text-left">Group ID</th>
              <th class="py-3 px-4 font-semibold">Group Name</th>
              <th class="py-3 px-4 font-semibold text-center">Students</th>
              <th class="py-3 px-4 font-semibold text-center">Actions</th>
            </tr>
          </thead>

          <tbody class="bg-white divide-y divide-gray-100">
            <template v-for="g in groups" :key="g.Group_Id">

              <!-- MAIN GROUP ROW -->                      
              <tr class="hover:bg-gray-50 transition cursor-pointer">
                <!-- GROUP ID -->
                <td class="px-4 py-4 font-medium text-gray-600">
                  {{ g.Group_Id }}
                </td>
                <!-- GROUP NAME -->
                <td class="px-4 py-4 font-medium text-gray-800">
                  {{ g.Group_Name }}
                </td> 
                <!-- STUDENT COUNT -->
                <td class="px-4 py-4 text-center">
                  <span
                    class="px-3 py-1 rounded-full text-sm font-semibold"
                    :class="(applicants[g.Group_Id]?.length || 0)
                      ? 'bg-green-100 text-green-700'
                      : 'bg-gray-200 text-gray-600'"
                  >
                    👥 {{ applicants[g.Group_Id]?.length || 0 }}
                  </span>
                </td>

                <!-- ACTIONS -->
                <td class="px-4 py-4 flex justify-center gap-2">
                  <button
                    @click="toggleView(g.Group_Id)"
                    class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg shadow hover:scale-105 transition"
                  >
                    {{ expandedGroup === g.Group_Id ? "Hide" : "View" }}
                  </button>

                  <button
                    @click="deleteGroup(g.Group_Id)"
                    class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg shadow hover:scale-105 transition"
                  >
                    Delete
                  </button>
                </td>
              </tr>

              <!-- EXPANDED STUDENT LIST UNDER SAME GROUP -->
              <tr v-if="expandedGroup === g.Group_Id" class="bg-gray-50">
                <td colspan="4" class="p-6">

                  <h3 class="text-lg font-bold mb-4 text-gray-700">
                    Students in {{ g.Group_Name }}
                  </h3>

                  <!-- EXPANDED STUDENT LIST -->
                  <div class="mt-4">

                    <!-- IF STUDENTS EXIST -->
                    <div v-if="applicants[g.Group_Id]?.length" class="rounded-2xl shadow-md border bg-white overflow-hidden">

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
                            v-for="a in applicants[g.Group_Id]"
                            :key="a.Applicant_Id"
                            class="hover:bg-blue-50 transition cursor-pointer"
                          >
                            <td class="px-4 py-3 font-medium text-gray-800">
                              {{ a.Full_Name }}
                            </td>

                            <td class="px-4 py-3 text-gray-700">
                              {{ a.Email }}
                            </td>

                            <td class="px-4 py-3 text-center">
                              <button
                                @click="removeApplicant(g.Group_Id, a.Applicant_Id)"
                                class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-full text-sm shadow hover:scale-105 transition">
                                Remove
                              </button>
                            </td>
                          </tr>
                        </tbody>
                      </table>

                    </div>

                    <!-- IF EMPTY -->
                    <p v-else class="text-gray-500 italic text-center py-4">
                      No students in this group
                    </p>

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
import { ref, onMounted, computed } from "vue"
import axios from "@/utils/axiosInstance"

const emit = defineEmits(["toast"])

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
  if (!groupName.value.trim()) {
    emit("toast", {
      message: "Group name is required",
      type: "error"
    })
    return
  }

  try {
    await axios.post("/groups/create", {
      group_name: groupName.value,
      role,
      email
    })

    groupName.value = ""
    await loadGroups()

    // ✅ SUCCESS TOAST
    emit("toast", {
      message: "Student group created successfully!",
      type: "success"
    })

  } catch (err) {
    emit("toast", {
      message: err.response?.data?.error || "Error creating student group",
      type: "error"
    })
  }
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

  try {
    await axios.delete(`/groups/${groupId}`)

    expandedGroup.value = null
    await loadGroups()

    // ✅ SUCCESS TOAST
    emit("toast", {
      message: "Student group deleted successfully!",
      type: "success"
    })

  } catch (err) {
    emit("toast", {
      message: err.response?.data?.error || "Error deleting student group",
      type: "error"
    })
  }
}

onMounted(loadGroups)
</script>
