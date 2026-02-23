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

    <!-- OUTER WRAPPER CARD -->
    <div class="bg-white/80 backdrop-blur-sm shadow-xl rounded-2xl p-8 border border-white/20">

      <!-- HEADER -->
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-800 tracking-wide">
          Student Groups Management
        </h2>

        <div class="flex items-center gap-4">
          <!-- CREATE GROUP BUTTON -->
          <button
            v-if="isAdmin"
            @click="showCreateModal = true"
            class="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6 py-3 
                  rounded-full shadow-lg transition hover:scale-105"
          >
            Create Group
          </button>

          <!-- ACTIVE / ALL TOGGLE -->
          <div class="flex items-center bg-gray-100 rounded-full p-1 shadow-inner">
            <button
              @click="showDisabled = false"
              :class="[
                'px-4 py-2 text-sm font-semibold rounded-full transition-all',
                !showDisabled
                  ? 'bg-white text-blue-600 shadow'
                  : 'text-gray-600 hover:text-gray-800'
              ]"
            >
              Active Only
            </button>

            <button
              @click="showDisabled = true"
              :class="[
                'px-4 py-2 text-sm font-semibold rounded-full transition-all',
                showDisabled
                  ? 'bg-white text-blue-600 shadow'
                  : 'text-gray-600 hover:text-gray-800'
              ]"
            >
              All Groups
            </button>
          </div>
        </div>
      </div>
      <transition name="fade">
        <p
          v-if="showDisabled"
          class="text-xs text-gray-500 mb-2 text-right"
        >
          Disabled groups are shown in grey
        </p>
      </transition>

      <!-- INNER CARD -->
      <div class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-200 p-6">

        <!-- SEARCH FILTER INPUT -->
        <div class="mb-6 flex gap-3">
          <input
            v-model="searchQuery"
            placeholder="🔍 Search groups..."
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
            <template v-for="g in searchedGroups" :key="g.Group_Id">

              <!-- MAIN GROUP ROW -->                      
              <tr :class="['transition-colors',g.Is_Active === 0 ? 'opacity-50 bg-gray-100' : 'hover:bg-gray-50']">
                <td class="px-4 py-4 font-medium text-gray-600">
                  {{ g.Group_Id }}
                </td>
                <td class="px-4 py-4 font-medium text-gray-800">
                  {{ g.Group_Name }}
                </td> 
                <td class="px-4 py-4 text-center">
                  <span
                    class="px-3 py-1 rounded-full text-sm font-semibold"
                    :class="g.Applicant_Count > 0
                      ? 'bg-green-100 text-green-700'
                      : 'bg-gray-200 text-gray-600'"
                  >
                    👥 {{ g.Applicant_Count }}
                  </span>
                </td>

                <td class="px-4 py-4 flex justify-center gap-2">
                  <button
                    @click="toggleView(g.Group_Id)"
                    :disabled="g.Is_Active === 0"
                    class="disabled:cursor-not-allowed disabled:opacity-50 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg shadow hover:scale-105 transition"
                  >
                    {{ expandedGroup === g.Group_Id ? "Hide" : "View" }}
                  </button>

                  <button
                    @click="toggleGroupStatus(g)"
                    :class="g.Is_Active === 1
                      ? 'bg-red-500 hover:bg-red-600'
                      : 'bg-green-500 hover:bg-green-600'"
                    class="text-white px-4 py-2 rounded-lg shadow hover:scale-105 transition"
                  >
                    {{ g.Is_Active === 1 ? 'Disable' : 'Enable' }}
                  </button>
                </td>
              </tr>

              <!-- EXPANDED STUDENT LIST -->
              <tr
                v-if="expandedGroup === g.Group_Id && applicants[g.Group_Id]"
                :key="`expanded-${g.Group_Id}-${fetchTimestamp}`"
                class="bg-gray-50"
              >
                <td colspan="4" class="p-6">

                  <h3 class="text-lg font-bold mb-4 text-gray-700">
                    Students in {{ g.Group_Name }}
                  </h3>

                  <div class="mt-4">

                    <!-- STUDENT LIST -->
                    <div v-if="applicants[g.Group_Id]?.length > 0" class="rounded-2xl shadow-md border bg-white overflow-hidden">

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
                            :key="`applicant-${a.Applicant_Id}-${fetchTimestamp}`"
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
                                :disabled="g.Is_Active === 0"  
                                :class="g.Is_Active === 0    ? 
                                'bg-red-300 cursor-not-allowed'    
                                : 'bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-full text-sm shadow hover:scale-105 transition'">
                                Remove
                              </button>
                            </td>
                          </tr>
                        </tbody>
                      </table>

                    </div>

                    <!-- EMPTY STATE -->
                    <p v-else class="text-gray-500 italic text-center py-4">
                      No students in this group
                    </p>

                  </div>

                </td>
              </tr>

            </template>

            <!-- NO RESULTS STATE -->
            <tr v-if="searchedGroups.length === 0">
              <td colspan="4" class="text-center py-8 text-gray-500 italic">
                No groups found matching "{{ searchQuery }}"
              </td>
            </tr>

          </tbody>

        </table>

      </div>
    </div>

    <!-- ===================== CREATE GROUP MODAL ===================== -->
    <div
      v-if="showCreateModal"
      class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-[9999] p-4"
      @click.self="showCreateModal = false"
    >
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md p-8 animate-fadeIn">
        
        <!-- Modal Header -->
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-2xl font-bold text-gray-800">Create Student Group</h3>
          <button
            @click="showCreateModal = false"
            class="w-8 h-8 flex items-center justify-center rounded-full bg-gray-100 hover:bg-gray-200 transition text-gray-500 text-lg font-bold"
          >
            ×
          </button>
        </div>

        <!-- Group Name Input -->
        <div class="mb-6">
          <label class="block text-sm font-semibold text-gray-700 mb-2">Group Name</label>
          <input
            v-model="newGroupName"
            placeholder="Enter group name..."
            @keyup.enter="createGroup"
            class="w-full px-4 py-3 rounded-xl border border-gray-300 bg-purple-50 focus:bg-white 
                   focus:ring-2 focus:ring-blue-400 focus:border-blue-400 transition outline-none text-gray-800"
            autofocus
          />
        </div>

        <!-- Buttons -->
        <div class="flex justify-end gap-3">
          <button
            @click="showCreateModal = false; newGroupName = ''"
            class="px-6 py-2.5 rounded-full bg-gray-200 text-gray-700 font-semibold hover:bg-gray-300 transition"
          >
            Cancel
          </button>
          <button
            @click="createGroup"
            :disabled="!newGroupName.trim()"
            class="px-6 py-2.5 rounded-full bg-blue-600 text-white font-semibold 
                   hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed shadow-md"
          >
            Create Group
          </button>
        </div>
      </div>
    </div>
    <!-- ============================================================== -->

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import axios from "@/utils/axiosInstance"
import { watch } from "vue"

const emit = defineEmits(["toast"])

const showDisabled = ref(false)
const newGroupName = ref("")
const searchQuery = ref("")
const showCreateModal = ref(false)
const groups = ref([])
const applicants = ref({})
const expandedGroup = ref(null)
const fetchTimestamp = ref(Date.now())

const role =
  (localStorage.getItem("active_role") || "").toLowerCase() === "admin"
    ? "Admin"
    : "Faculty"

const isAdmin = computed(() => role === "Admin")

const email = localStorage.getItem("email")

watch(showDisabled, () => {
  loadGroups()
})

const filteredGroups = computed(() => {
  const list = showDisabled.value
    ? groups.value
    : groups.value.filter(g => g.Is_Active === 1)

  return [...list].sort((a, b) => b.Is_Active - a.Is_Active)
})

const searchedGroups = computed(() => {
  if (!searchQuery.value.trim()) return filteredGroups.value
  const q = searchQuery.value.toLowerCase()
  return filteredGroups.value.filter(g =>
    g.Group_Name.toLowerCase().includes(q) ||
    String(g.Group_Id).includes(q)
  )
})

/* ENABLE / DISABLE GROUP */
const toggleGroupStatus = async (group) => {
  const action = group.Is_Active === 1 ? 'disable' : 'enable'

  if (!confirm(`Are you sure you want to ${action} this group?`)) return

  try {
    await axios.put(`/groups/toggle-status/${group.Group_Id}`)

    emit("toast", {
      message: `Group ${action}d successfully`,
      type: "success"
    })

    await loadGroups()

  } catch (err) {
    console.error("Toggle group status failed:", err)
    emit("toast", {
      message: "Failed to update group status",
      type: "error"
    })
  }
}

/* LOAD GROUPS */
const loadGroups = async () => {
  try {
    const res = await axios.get("/groups", {
      params: { role, email, show_all: showDisabled.value }
    })

    if (res.data.success) {
      groups.value = res.data.groups
      expandedGroup.value = null
      applicants.value = {}
      expandedGroup.value = null
      fetchTimestamp.value = Date.now()
    }
  } catch (err) {
    console.error("Error loading groups:", err)
    emit("toast", {
      message: "Error loading groups",
      type: "error"
    })
  }
}

/* CREATE GROUP */
const createGroup = async () => {
  if (!newGroupName.value.trim()) {
    emit("toast", {
      message: "Group name is required",
      type: "error"
    })
    return
  }

  try {
    await axios.post("/groups/create", {
      group_name: newGroupName.value,
      role,
      email
    })

    newGroupName.value = ""
    showCreateModal.value = false
    await loadGroups()

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
const toggleView = async (groupId) => {
  if (expandedGroup.value === groupId) {
    expandedGroup.value = null
    return
  }

  expandedGroup.value = groupId

  try {
    const res = await axios.get(`/groups/${groupId}/applicants`, {
      params: { _t: Date.now() }
    })
    
    applicants.value = {
      ...applicants.value,
      [groupId]: res.data.success ? res.data.applicants : []
    }
    
    fetchTimestamp.value = Date.now()
      
  } catch (err) {
    console.error("Error fetching applicants:", err)
    applicants.value[groupId] = []
    
    emit("toast", {
      message: "Error loading students",
      type: "error"
    })
  }
}

/* REMOVE APPLICANT */
const removeApplicant = async (groupId, applicantId) => {
  if (!confirm("Remove applicant from this group?")) return

  try {
    await axios.post("/groups/remove-applicant", {
      group_id: groupId,
      applicant_id: applicantId
    })

    expandedGroup.value = null
    await loadGroups()
    await toggleView(groupId)

    emit("toast", {
      message: "Student removed from group successfully!",
      type: "success"
    })

  } catch (err) {
    emit("toast", {
      message: err.response?.data?.error || "Error removing student",
      type: "error"
    })
  }
}

/* DELETE GROUP */
const deleteGroup = async (groupId) => {
  if (!confirm("Delete this group permanently?")) return

  try {
    await axios.delete(`/groups/${groupId}`)

    expandedGroup.value = null
    await loadGroups()

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

<style scoped>
@keyframes fadeIn {
  from { transform: translateY(16px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
.animate-fadeIn {
  animation: fadeIn 0.2s ease-out;
}
</style>