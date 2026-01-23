<template>
  <div class="space-y-6">

    <!-- Header Card -->
    <div class="bg-white/80 backdrop-blur-sm shadow-xl rounded-2xl p-8 border border-white/20">

      <!-- Page Title -->
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-800">Applicant Groups</h2>

        <button
          @click="createGroup"
          class="bg-blue-600 hover:bg-blue-800 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all hover:scale-105"
        >
          Create Group
        </button>
      </div>

      <!-- Create Group Input -->
      <div class="mb-8">
        <input
          v-model="groupName"
          type="text"
          placeholder="Enter Group Name"
          class="w-full max-w-sm px-4 py-3 rounded-xl border border-gray-300 bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <!-- Groups Table -->
      <div class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-200">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gradient-to-r from-blue-50 to-blue-100">
              <tr>
                <th class="py-4 px-6 font-semibold text-blue-900 text-left">Group Name</th>
                <th class="py-4 px-6 font-semibold text-blue-900 text-left">Created By</th>
                <th class="py-4 px-6 font-semibold text-blue-900 text-center">Actions</th>
              </tr>
            </thead>

            <tbody class="bg-white divide-y divide-gray-100">

              <!-- Each Group -->
              <template v-for="g in groups" :key="g.Group_Id">
                <tr class="hover:bg-gray-50 transition-colors">
                  <td class="py-4 px-6 text-gray-900">{{ g.Group_Name }}</td>
                  <td class="py-4 px-6">{{ g.Faculty_Email }}</td>

                  <td class="py-4 px-6 text-center">
                    <button
                      @click="toggleView(g.Group_Id)"
                      class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm shadow transition hover:scale-105"
                    >
                      {{ expandedGroup === g.Group_Id ? "Hide" : "View" }}
                    </button>
                  </td>
                </tr>

                <!-- Expanded Row -->
                <tr v-if="expandedGroup === g.Group_Id">
                  <td colspan="3" class="bg-gray-50 px-6 py-6">

                    <h3 class="text-xl font-semibold text-gray-700 mb-4">
                      Applicants in {{ g.Group_Name }}
                    </h3>

                    <!-- Applicants Table -->
                    <table
                      v-if="applicants[g.Group_Id]?.length"
                      class="w-full border border-gray-300 rounded-xl overflow-hidden"
                    >
                      <thead class="bg-gray-200">
                        <tr>
                          <th class="px-4 py-2 font-medium text-left">Name</th>
                          <th class="px-4 py-2 font-medium text-left">Email</th>
                          <th class="px-4 py-2 font-medium text-left">Phone</th>
                          <th class="px-4 py-2 font-medium text-left">Gender</th>
                        </tr>
                      </thead>

                      <tbody class="bg-white divide-y divide-gray-100">
                        <tr
                          v-for="a in applicants[g.Group_Id]"
                          :key="a.Applicant_Id"
                          class="hover:bg-gray-100 transition"
                        >
                          <td class="px-4 py-2">{{ a.Full_Name }}</td>
                          <td class="px-4 py-2">{{ a.Email }}</td>
                          <td class="px-4 py-2">{{ a.Phone }}</td>
                          <td class="px-4 py-2">{{ a.Gender }}</td>
                        </tr>
                      </tbody>
                    </table>

                    <!-- No Applicants -->
                    <p v-else class="text-gray-500 italic mt-2">
                      No applicants in this group.
                    </p>

                  </td>
                </tr>

              </template>

            </tbody>
          </table>
        </div>
      </div>

    </div>

    <!-- No Groups Text -->
    <p v-if="!groups.length" class="text-gray-500 text-center text-lg">
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
const emit = defineEmits(["toast"])

// ROLE (FIXED)
const rawRole = (localStorage.getItem("active_role") || "").toLowerCase()
const activeRole = rawRole === "admin" ? "Admin" : "Faculty"

// EMAIL (FIXED)
const email = localStorage.getItem("email")

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
  console.log("Creating Group With:", {
    group_name: groupName.value,
    role: activeRole,
    email
  });

  if (!groupName.value.trim()) {
    emit("toast", { message: "Group name cannot be empty!", type: "error" });
    return;
  }

  if (!email) {
    emit("toast", { message: "Logged-in email not found! Please login again.", type: "error" });
    return;
  }

  try {
    const res = await axios.post("/groups/create", {
      group_name: groupName.value,
      role: activeRole,
      email
    });

    if (res.data.success) {
      emit("toast", {
        message: "Group created successfully!",
        type: "success"
      });

      groupName.value = "";
      loadGroups();
    } else {
      emit("toast", {
        message: res.data.message || "Unable to create group.",
        type: "error"
      });
    }
  } catch (err) {
    emit("toast", {
      message: err.response?.data?.message || "Something went wrong.",
      type: "error"
    });
  }
};


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
