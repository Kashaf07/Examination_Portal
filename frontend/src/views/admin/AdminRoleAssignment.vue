<template>
  <div class="space-y-6">

    <!-- Header -->
    <div class="bg-white/80 backdrop-blur-sm shadow-xl rounded-2xl p-8 border border-white/20">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-800">Role Assignment</h2>
      </div>

      <!-- Table -->
      <div class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-200">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gradient-to-r from-blue-50 to-blue-100">
              <tr>
                <th class="py-4 px-6 font-semibold text-blue-900">#</th>
                <th class="py-4 px-6 font-semibold text-blue-900">Designation</th>
                <th class="py-4 px-6 font-semibold text-blue-900">Assigned Role</th>
                <th class="py-4 px-6 font-semibold text-blue-900">Access Level</th>
                <th class="py-4 px-6 font-semibold text-blue-900">Actions</th>
              </tr>
            </thead>

            <tbody class="bg-white divide-y divide-gray-100">
              <tr v-for="(row, index) in tableData" :key="row.Designation_Id"
                  class="hover:bg-gray-50 transition-colors">

                <td class="py-4 px-6">{{ index + 1 }}</td>
                <td class="py-4 px-6">{{ row.Designation_Name }}</td>
                <td class="py-4 px-6">{{ row.Role_Name || "Not Assigned" }}</td>
                <td class="py-4 px-6">{{ row.Access_Level || "-" }}</td>

                <td class="py-4 px-6">
                  <button
                    @click="openRoleModal(row)"
                    class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm shadow transition hover:scale-105"
                  >
                    Assign Role
                  </button>
                </td>

              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Assign Role Modal -->
    <div v-if="showModal"
         class="fixed inset-0 bg-black/40 backdrop-blur-md flex items-center justify-center z-[1000]">

      <div class="bg-white rounded-3xl shadow-2xl p-8 w-full max-w-md">
        <h3 class="text-2xl font-bold text-gray-800 mb-8 text-center">
          Assign Role
        </h3>

        <div class="space-y-4">
          <div>
            <label class="font-semibold text-gray-700 block mb-2">Designation</label>
            <input 
              class="w-full px-4 py-3 rounded-xl border bg-gray-100"
              :value="selectedItem.Designation_Name"
              disabled />
          </div>

          <div>
            <label class="font-semibold text-gray-700 block mb-2">Select Role</label>
            <select v-model="selectedRoleId"
                    class="w-full px-4 py-3 rounded-xl border bg-purple-50 focus:bg-white focus:ring-2">
              <option value="">Select Role</option>
              <option v-for="role in rolesList" 
                      :key="role.Role_Id"
                      :value="role.Role_Id">
                {{ role.Role_Name }} (Level {{ role.Access_Level }})
              </option>
            </select>
          </div>
        </div>

        <div class="flex justify-center gap-4 mt-8">
          <button @click="closeModal"
                  class="px-8 py-3 bg-gray-200 text-gray-700 rounded-full hover:bg-gray-300">
            Cancel
          </button>

          <button @click="saveRoleAssignment"
                  class="px-8 py-3 bg-blue-600 text-white rounded-full hover:bg-blue-700">
            Save
          </button>
        </div>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const emit = defineEmits(["toast"]);
const API = "http://localhost:5000/api/admin";

// STATE
const tableData = ref([]);
const rolesList = ref([]);

const showModal = ref(false);
const selectedItem = ref({});
const selectedRoleId = ref("");

// FETCH DESIGNATION + ROLE MAPPING
const fetchDesignationRoles = async () => {
  const res = await axios.get(`${API}/designation-roles`);
  tableData.value = res.data.data;
};

// FETCH AVAILABLE ROLES
const fetchRoles = async () => {
  const res = await axios.get(`${API}/roles`);
  rolesList.value = res.data.data;
};

// OPEN ROLE MODAL
const openRoleModal = (row) => {
  selectedItem.value = row;
  selectedRoleId.value = row.Role_Id || "";
  showModal.value = true;
};

// CLOSE MODAL
const closeModal = () => {
  showModal.value = false;
};

// SAVE ROLE ASSIGNMENT
const saveRoleAssignment = async () => {
  if (!selectedRoleId.value) {
    emit("toast", { message: "Please select a role", type: "error" });
    return;
  }

  try {
    await axios.put(`${API}/designation-roles/${selectedItem.value.Designation_Id}`, {
      role_id: selectedRoleId.value
    });

    emit("toast", { message: "Role assigned successfully!", type: "success" });

    showModal.value = false;
    fetchDesignationRoles();

  } catch (err) {
    emit("toast", {
      message: err.response?.data?.error || "Error saving role",
      type: "error"
    });
  }
};

// MOUNT
onMounted(() => {
  fetchDesignationRoles();
  fetchRoles();
});
</script>
