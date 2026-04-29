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

          <div class="flex flex-col items-start">
            <div class="flex items-center bg-gray-100 rounded-full p-1 shadow-inner">
              <button
                @click="filterMode = 'active'"
                :class="['px-4 py-2 text-sm font-semibold rounded-full transition-all',
                  filterMode === 'active' ? 'bg-white text-blue-600 shadow' : 'text-gray-600']">
                Active Only
              </button>
              <button
                @click="filterMode = 'all'"
                :class="['px-4 py-2 text-sm font-semibold rounded-full transition-all',
                  filterMode === 'all' ? 'bg-white text-blue-600 shadow' : 'text-gray-600']">
                All Admins
              </button>
              <button
                @click="filterMode = 'inactive'"
                :class="['px-4 py-2 text-sm font-semibold rounded-full transition-all',
                  filterMode === 'inactive' ? 'bg-white text-blue-600 shadow' : 'text-gray-600']">
                Inactive Only
              </button>
            </div>
            <p v-if="filterMode === 'all'" class="mt-1 text-xs text-gray-500 pl-2">
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
                :class="['hover:bg-gray-50 transition', admin.Is_Active === 0 ? 'opacity-50 bg-gray-100' : '']">
                <td class="py-4 px-6">{{ i + 1 }}</td>
                <td class="py-4 px-6">{{ admin.Name }}</td>
                <td class="py-4 px-6">
                  {{ admin.Email }}
                  <span
                    v-if="admin.Is_Super_Admin === 1"
                    class="ml-2 px-2 py-1 text-xs bg-yellow-200 text-yellow-800 rounded-full">
                    Super Admin 👑
                  </span>
                </td>
                <td class="py-4 px-6 space-x-3">
                  <button
                    @click="openEditModal(admin)"
                    class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm transition hover:scale-105 shadow-md">
                    Edit
                  </button>
                  <button
                    @click="toggleAdminStatus(admin)"
                    :disabled="admin.Is_Super_Admin === 1"
                    :title="admin.Is_Super_Admin === 1 ? 'Super Admin cannot be disabled' : ''"
                    :class="['text-white px-4 py-2 rounded-lg text-sm shadow transition hover:scale-105',
                      admin.Is_Super_Admin === 1
                        ? 'bg-gray-300 cursor-not-allowed'
                        : (Number(admin.Is_Active) === 1
                          ? 'bg-red-500 hover:bg-red-600'
                          : 'bg-green-500 hover:bg-green-600')]">
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
      class="fixed inset-0 bg-black/60 backdrop-blur-md flex items-center justify-center z-[9999] p-4">
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
                class="w-full px-4 py-3 rounded-xl border bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"/>
            </div>

            <div>
              <label class="font-semibold text-gray-700 mb-2 block">Email</label>
              <input
                v-model="form.Email"
                type="email"
                required
                class="w-full px-4 py-3 rounded-xl border bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"/>
            </div>

            <div v-if="!isEdit">
              <label class="font-semibold text-gray-700 mb-2 block">Password</label>
              <input
                v-model="form.Password"
                type="password"
                required
                class="w-full px-4 py-3 rounded-xl border bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"/>
            </div>

            <!-- ✅ Super Admin checkbox — only visible in Edit mode, only if current user is Super Admin -->
            <div
              v-if="isEdit && currentUserIsSuperAdmin"
              class="flex items-center gap-3 p-4 rounded-xl border bg-yellow-50 border-yellow-200">
              <input
                type="checkbox"
                id="superAdminCheckbox"
                v-model="form.Is_Super_Admin_Bool"
                :disabled="form.Admin_ID === currentAdminId"
                class="w-4 h-4 accent-yellow-500 cursor-pointer"/>
              <label
                for="superAdminCheckbox"
                :class="['text-sm font-semibold select-none',
                  form.Admin_ID === currentAdminId ? 'text-gray-400 cursor-not-allowed' : 'text-yellow-800 cursor-pointer']">
                Super Admin 👑
                <span v-if="form.Admin_ID === currentAdminId" class="text-xs font-normal text-gray-400 ml-1">
                  (cannot change your own)
                </span>
              </label>
            </div>

          </div>

          <div class="flex justify-center mt-8 space-x-4">
            <button
              type="button"
              @click="closeModal"
              class="px-8 py-3 bg-gray-200 text-gray-700 rounded-full hover:bg-gray-300 transition hover:scale-105">
              Cancel
            </button>
            <button
              type="submit"
              class="px-8 py-3 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition hover:scale-105">
              {{ isEdit ? "Update" : "Add" }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Confirmation Modal -->
    <ConfirmationModal
      :is-open="showConfirmModal"
      :title="confirmModalConfig.title"
      :message="confirmModalConfig.message"
      :variant="confirmModalConfig.variant"
      @confirm="confirmModalConfig.onConfirm"
      @close="showConfirmModal = false"/>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import axios from "axios";
import ConfirmationModal from "@/components/ConfirmationModal.vue";

const emit = defineEmits(["toast"]);

const API = `http://${window.location.hostname}:5000/api`;

// ── Current logged-in admin info (read from localStorage) ──
const currentAdminEmail = ref(localStorage.getItem("email") || "");
const currentAdminId    = ref(Number(localStorage.getItem("admin_id")) || null);

// Is the currently logged-in admin a Super Admin?
// We derive this from the loaded admins list so it's always in sync.
const currentUserIsSuperAdmin = computed(() => {
  const me = admins.value.find(a => a.Email === currentAdminEmail.value);
  return me ? Number(me.Is_Super_Admin) === 1 : false;
});

// ── Filter ──
const filterMode = ref("active");
const filteredAdmins = computed(() => {
  if (filterMode.value === "active")   return admins.value.filter(a => Number(a.Is_Active) === 1);
  if (filterMode.value === "inactive") return admins.value.filter(a => Number(a.Is_Active) === 0);
  return admins.value;
});

// ── Data ──
const admins        = ref([]);
const showModal     = ref(false);
const isEdit        = ref(false);

const showConfirmModal  = ref(false);
const confirmModalConfig = ref({ title: "", message: "", variant: "default", onConfirm: null });

const form = ref({
  Admin_ID: null,
  Name: "",
  Email: "",
  Password: "",
  Is_Super_Admin: 0,
  Is_Super_Admin_Bool: false   // checkbox binding
});

// ── Fetch ──
const fetchAdmins = async () => {
  try {
    const res = await axios.get(`${API}/admin/admins`);
    admins.value = res.data;
  } catch {
    emit("toast", { message: "Error fetching admin list", type: "error" });
  }
};

// ── Modal ──
const openAddModal = () => {
  isEdit.value = false;
  form.value = { Admin_ID: null, Name: "", Email: "", Password: "", Is_Super_Admin: 0, Is_Super_Admin_Bool: false };
  showModal.value = true;
};

const openEditModal = (admin) => {
  isEdit.value = true;
  form.value = {
    ...admin,
    Password: "",
    Is_Super_Admin_Bool: Number(admin.Is_Super_Admin) === 1
  };
  showModal.value = true;
};

const closeModal = () => { showModal.value = false; };

// ── CRUD ──
const addAdmin = async () => {
  try {
    await axios.post(`${API}/admin/admins`, form.value);
    emit("toast", { message: "Admin added successfully!", type: "success" });
    await fetchAdmins();
    closeModal();
  } catch (err) {
    emit("toast", { message: err.response?.data?.error || "Error adding admin", type: "error" });
  }
};

const updateAdmin = async () => {
  try {
    // 1. Save name/email as usual
    await axios.put(`${API}/admin/admins/${form.value.Admin_ID}`, form.value);

    // 2. If Super Admin checkbox changed, call the dedicated route
    const originalSuperAdmin = Number(
      admins.value.find(a => a.Admin_ID === form.value.Admin_ID)?.Is_Super_Admin
    ) === 1;
    const newSuperAdmin = form.value.Is_Super_Admin_Bool;

    if (currentUserIsSuperAdmin.value && newSuperAdmin !== originalSuperAdmin) {
      await axios.put(`${API}/admin/admins/toggle-super/${form.value.Admin_ID}`, {
        requested_by: currentAdminEmail.value
      });
    }

    emit("toast", { message: "Admin updated successfully!", type: "success" });
    await fetchAdmins();
    closeModal();
  } catch (err) {
    emit("toast", { message: err.response?.data?.error || "Error updating admin", type: "error" });
  }
};

const toggleAdminStatus = (admin) => {
  const action = admin.Is_Active ? "disable" : "enable";
  confirmModalConfig.value = {
    title: `${action.charAt(0).toUpperCase() + action.slice(1)} Admin`,
    message: `Are you sure you want to ${action} this admin?`,
    variant: action === "disable" ? "danger" : "default",
    onConfirm: async () => {
      try {
        await axios.put(`${API}/admin/admins/toggle-status/${admin.Admin_ID}`);
        await fetchAdmins();
        emit("toast", { message: `Admin ${action}d successfully`, type: "success" });
      } catch (err) {
        emit("toast", { message: err.response?.data?.error || "Failed to update admin status", type: "error" });
      }
    }
  };
  showConfirmModal.value = true;
};

onMounted(fetchAdmins);
</script>