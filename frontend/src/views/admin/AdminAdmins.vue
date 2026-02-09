<template>
  <div class="space-y-6">

    <!-- ----------- Header ----------- -->
    <div class="bg-white/80 backdrop-blur-sm shadow-xl rounded-2xl p-8 border border-white/20">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-800">Admins Management</h2>

        <div class="flex items-center gap-4">
          <button
            @click="openAddModal"
            class="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition hover:scale-105">
            Add Admin
          </button>

          <!-- Toggle + helper grouped together -->
          <div class="flex flex-col items-start">
            <div class="flex items-center bg-gray-100 rounded-full p-1 shadow-inner">
              <button
                @click="showDisabled = false"
                :class="[
                  'px-4 py-2 text-sm font-semibold rounded-full transition-all',
                  !showDisabled ? 'bg-white text-blue-600 shadow' : 'text-gray-600'
                ]">
                Active Only
              </button>

              <button
                @click="showDisabled = true"
                :class="[
                  'px-4 py-2 text-sm font-semibold rounded-full transition-all',
                  showDisabled ? 'bg-white text-blue-600 shadow' : 'text-gray-600'
                ]">
                All Admins
              </button>
            </div>

            <!-- ✅ Helper text exactly below toggle -->
            <p
              v-if="showDisabled"
              class="mt-1 text-xs text-gray-500 pl-2">
              Disabled admins are shown in grey
            </p>
          </div>
        </div>

      </div>

      <!-- ----------- Admins Table ----------- -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gradient-to-r from-blue-50 to-blue-100 border-b border-blue-200">
              <tr>
                <th class="py-4 px-6 text-left font-semibold text-blue-900">ID</th>
                <th class="py-4 px-6 text-left font-semibold text-blue-900">Name</th>
                <th class="py-4 px-6 text-left font-semibold text-blue-900">Email</th>
                <th class="py-4 px-6 text-left font-semibold text-blue-900">Actions</th>
              </tr>
            </thead>

            <tbody class="bg-white divide-y divide-gray-100">
              <tr
                v-for="(admin, i) in filteredAdmins"
                :key="admin.Admin_ID"
                :class="['hover:bg-gray-50 transition',admin.Is_Active === 0 ? 'opacity-50 bg-gray-100' : '']"
              >
                <td class="py-4 px-6">{{ i + 1 }}</td>
                <td class="py-4 px-6">{{ admin.Name }}</td>
                <td class="py-4 px-6">{{ admin.Email }}</td>

                <td class="py-4 px-6 space-x-3">
                  <button
                    @click="openEditModal(admin)"
                    class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm transition hover:scale-105 shadow-md"
                  >
                    Edit
                  </button>
                  <button
                    @click="toggleAdminStatus(admin)"
                    :class="Number(admin.Is_Active) === 1
                      ? 'bg-red-500 hover:bg-red-600'
                      : 'bg-green-500 hover:bg-green-600'"
                    class="text-white px-4 py-2 rounded-lg text-sm shadow transition hover:scale-105">
                    {{ Number(admin.Is_Active) === 1 ? 'Disable' : 'Enable' }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ----------- Add/Edit Modal ----------- -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black/60 backdrop-blur-md flex items-center justify-center z-[9999] p-4"
    >
      <div class="bg-white shadow-2xl rounded-3xl p-8 w-full max-w-md">
        <h3 class="text-2xl font-bold text-gray-800 mb-8 text-center">
          {{ isEdit ? "Edit Admin" : "Add Admin" }}
        </h3>
        <form @submit.prevent="isEdit ? updateAdmin() : addAdmin()">
          <div class="space-y-4">

            <div>
              <label class="font-semibold text-gray-700 mb-2 block">Name</label>
              <input
                v-model="form.Name"
                required
                class="w-full px-4 py-3 rounded-xl border bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label class="font-semibold text-gray-700 mb-2 block">Email</label>
              <input
                v-model="form.Email"
                type="email"
                required
                class="w-full px-4 py-3 rounded-xl border bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div v-if="!isEdit">
              <label class="font-semibold text-gray-700 mb-2 block">Password</label>
              <input
                v-model="form.Password"
                type="password"
                required
                class="w-full px-4 py-3 rounded-xl border bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"
              />
            </div>

          </div>

          <div class="flex justify-center mt-8 space-x-4">
            <button
              type="button"
              @click="closeModal"
              class="px-8 py-3 bg-gray-200 text-gray-700 rounded-full hover:bg-gray-300 transition hover:scale-105"
            >
              Cancel
            </button>

            <button
              type="submit"
              class="px-8 py-3 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition hover:scale-105"
            >
              {{ isEdit ? "Update" : "Add" }}
            </button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import axios from "axios";

// Parent toast emitter
const emit = defineEmits(["toast"]);

const showDisabled = ref(false)

const filteredAdmins = computed(() => {
  if (showDisabled.value) return admins.value
  return admins.value.filter(a => Number(a.Is_Active) === 1)
})

// Simple reusable input component
const InputField = {
  props: ["label", "type", "modelValue", "required"],
  emits: ["update:modelValue"],
  template: `
    <div>
      <label class="block text-sm font-semibold text-gray-700 mb-2">{{ label }}</label>
      <input
        :type="type || 'text'"
        :value="modelValue"
        :required="required"
        @input="$emit('update:modelValue', $event.target.value)"
        class="w-full px-4 py-3 rounded-xl border bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"
      />
    </div>
  `
};

// ---------------- DATA ----------------
const API = "http://localhost:5000/api";

const admins = ref([]);
const showModal = ref(false);
const isEdit = ref(false);

const form = ref({
  Admin_ID: null,
  Name: "",
  Email: "",
  Password: ""
});

// ---------------- FETCH ADMIN LIST ----------------
const fetchAdmins = async () => {
  try {
    const res = await axios.get(`${API}/admin/admins`);
    admins.value = res.data;
  } catch {
    emit("toast", { message: "Error fetching admin list", type: "error" });
  }
};

// ---------------- MODAL ----------------
const openAddModal = () => {
  isEdit.value = false;
  form.value = { Admin_ID: null, Name: "", Email: "", Password: "" };
  showModal.value = true;
};

const openEditModal = (admin) => {
  isEdit.value = true;
  form.value = { ...admin, Password: "" };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

// ---------------- CRUD ACTIONS ----------------
const addAdmin = async () => {
  try {
    await axios.post(`${API}/admin/admins`, form.value);
    emit("toast", { message: "Admin added successfully!", type: "success" });
    await fetchAdmins();
    closeModal();
  } catch (err) {
    emit("toast", {
      message: err.response?.data?.error || "Error adding admin",
      type: "error",
    });
  }
};

const updateAdmin = async () => {
  try {
    await axios.put(`${API}/admin/admins/${form.value.Admin_ID}`, form.value);
    emit("toast", { message: "Admin updated successfully!", type: "success" });
    await fetchAdmins();
    closeModal();
  } catch (err) {
    emit("toast", {
      message: err.response?.data?.error || "Error updating admin",
      type: "error",
    });
  }
};

const toggleAdminStatus = async (admin) => {
  const action = admin.Is_Active ? "disable" : "enable"

  if (!confirm(`Are you sure you want to ${action} this admin?`)) return

  try {
    await axios.put(`${API}/admin/admins/toggle-status/${admin.Admin_ID}`)
    await fetchAdmins()

    emit("toast", {
      message: `Admin ${action}d successfully`,
      type: "success"
    })
  } catch (err) {
    emit("toast", {
      message: err.response?.data?.error || "Failed to update admin status",
      type: "error"
    })
  }
}

// ---------------- INIT ----------------
onMounted(fetchAdmins);
</script>
