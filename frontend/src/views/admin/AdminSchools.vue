<template>
  <div class="space-y-6">

    <!-- Header Section -->
    <div class="bg-white/80 backdrop-blur-sm shadow-xl rounded-2xl p-8 border border-white/20">

      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-800">Schools Management</h2>

        <div class="flex items-center gap-4">
          <button
            @click="openAddModal"
            class="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all hover:scale-105"
          >
            Add School
          </button>

          <div class="flex items-center bg-gray-100 rounded-full p-1 shadow-inner">
            <button
              @click="filterMode = 'active'"
              :class="[
                'px-4 py-2 text-sm font-semibold rounded-full transition-all',
                filterMode === 'active'
                  ? 'bg-white text-blue-600 shadow'
                  : 'text-gray-600 hover:text-gray-800'
              ]"
            >
              Active Only
            </button>

            <button
              @click="filterMode = 'all'"
              :class="[
                'px-4 py-2 text-sm font-semibold rounded-full transition-all',
                filterMode === 'all'
                  ? 'bg-white text-blue-600 shadow'
                  : 'text-gray-600 hover:text-gray-800'
              ]"
            >
              All Schools
            </button>

            <button
              @click="filterMode = 'inactive'"
              :class="[
                'px-4 py-2 text-sm font-semibold rounded-full transition-all',
                filterMode === 'inactive'
                  ? 'bg-white text-blue-600 shadow'
                  : 'text-gray-600 hover:text-gray-800'
              ]"
            >
              Inactive Only
            </button>
          </div>
        </div>
        </div>

        <transition name="fade">
          <p
            v-if="filterMode === 'all'"
            class="text-xs text-gray-500 mb-2 text-right"
          >
            Disabled schools are shown in grey
          </p>
        </transition>


      <!-- Schools Table -->
      <div class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-200">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gradient-to-r from-blue-50 to-blue-100">
              <tr>
                <th class="py-4 px-6 font-semibold text-blue-900">ID</th>
                <th class="py-4 px-6 font-semibold text-blue-900">School Name</th>
                <th class="py-4 px-6 font-semibold text-blue-900">Short Name</th>
                <th class="py-4 px-6 font-semibold text-blue-900">Actions</th>
              </tr>
            </thead>

            <tbody class="bg-white divide-y divide-gray-100">
              <tr
                v-for="(school, i) in filteredSchools"
                :key="school.School_Id"
                :class="['hover:bg-gray-50 transition-colors', school.Is_Active === 0 ? 'opacity-50 bg-gray-100' : '' ]"
              >
                <td class="py-4 px-6">{{ i + 1 }}</td>
                <td class="py-4 px-6">{{ school.School_Name }}</td>
                <td class="py-4 px-6">{{ school.School_Short }}</td>

                <td class="py-4 px-6 space-x-2">
                  <button
                    @click="openEditModal(school)"
                    class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm shadow transition hover:scale-105"
                  >
                    Edit
                  </button>

                  <button
                    @click="askToggleSchool(school)"
                    :class="Number(school.Is_Active) === 1
                      ? 'bg-red-500 hover:bg-red-600'
                      : 'bg-green-500 hover:bg-green-600'"
                    class="text-white px-4 py-2 rounded-lg text-sm shadow transition hover:scale-105"
                  >
                    {{ Number(school.Is_Active) === 1 ? 'Disable' : 'Enable' }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ----------- Add/Edit School Modal ----------- -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black/60 backdrop-blur-md flex items-center justify-center z-[9999]"
    >
      <div class="bg-white shadow-2xl rounded-3xl p-8 w-full max-w-md">

        <h3 class="text-2xl font-bold text-gray-800 mb-8 text-center">
          {{ isEdit ? "Edit School" : "Add School" }}
        </h3>

        <form @submit.prevent="isEdit ? updateSchool() : addSchool()">
          <div class="space-y-4">

            <div>
              <label class="font-semibold text-gray-700 mb-2 block">School Name</label>
              <input
                v-model="schoolForm.School_Name"
                required
                class="w-full px-4 py-3 rounded-xl border bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label class="font-semibold text-gray-700 mb-2 block">Short Name</label>
              <input
                v-model="schoolForm.School_Short"
                required
                class="w-full px-4 py-3 rounded-xl border bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"
              />
            </div>

          </div>

          <div class="flex justify-center space-x-4 mt-8">
            <button
              type="button"
              @click="closeModal"
              class="px-8 py-3 bg-gray-200 text-gray-700 rounded-full hover:bg-gray-300"
            >
              Cancel
            </button>

            <button
              type="submit"
              class="px-8 py-3 bg-blue-600 text-white rounded-full hover:bg-blue-700"
            >
              {{ isEdit ? "Update" : "Add" }}
            </button>
          </div>
        </form>
      </div>
    </div>

  </div>

  <!-- Confirmation Modal for Disable/Enable School -->
  <div
    v-if="showConfirmModal"
    class="fixed inset-0 z-[9999] flex items-center justify-center"
  >
    <div class="absolute inset-0 bg-black/60 backdrop-blur-md"></div>

    <div class="relative bg-white/95 backdrop-blur-sm rounded-3xl shadow-2xl p-8 max-w-md w-full mx-4 transform transition-all">
      <div class="text-center">

        <h3 class="text-2xl font-bold text-gray-900 mb-3">
          {{ schoolToToggle && Number(schoolToToggle.Is_Active) === 1 ? 'Disable School' : 'Enable School' }}
        </h3>

        <p class="text-sm text-gray-600 mb-8 leading-relaxed">
          Are you sure you want to
          {{ schoolToToggle && Number(schoolToToggle.Is_Active) === 1 ? 'disable' : 'enable' }}
          this school?
        </p>

        <div class="flex gap-4">
          <button
            @click="cancelConfirm"
            class="flex-1 py-3 bg-white text-gray-700 border border-gray-300 rounded-full hover:bg-gray-50 hover:border-gray-400 transition-all duration-300 font-semibold shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95"
          >
            Cancel
          </button>

          <button
            @click="confirmToggle"
            class="flex-1 py-3 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-all duration-300 font-semibold shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95"
          >
            OK
          </button>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import axios from "axios";

// Toast emitter to parent Admin.vue
const emit = defineEmits(["toast"]);

const API = `http://${window.location.hostname}:5000/api`;

const schoolsList = ref([]);

const showModal = ref(false);
const isEdit = ref(false);
const filterMode = ref('active');

// Confirmation modal state
const showConfirmModal = ref(false);
const schoolToToggle = ref(null);

const askToggleSchool = (school) => {
  schoolToToggle.value = school;
  showConfirmModal.value = true;
};

const cancelConfirm = () => {
  showConfirmModal.value = false;
  schoolToToggle.value = null;
};

const confirmToggle = async () => {
  const school = schoolToToggle.value;
  showConfirmModal.value = false;
  schoolToToggle.value = null;
  await toggleSchoolStatus(school);
};

const filteredSchools = computed(() => {
  if (filterMode.value === 'active') {
    return schoolsList.value.filter(s => Number(s.Is_Active) === 1);
  } else if (filterMode.value === 'inactive') {
    return schoolsList.value.filter(s => Number(s.Is_Active) === 0);
  }
  return schoolsList.value;
});

const schoolForm = ref({
  School_Id: null,
  School_Name: "",
  School_Short: "",
});

const openAddModal = () => {
  isEdit.value = false;
  showModal.value = true;
  schoolForm.value = { School_Id: null, School_Name: "", School_Short: "" };
};

const openEditModal = (data) => {
  isEdit.value = true;
  showModal.value = true;
  schoolForm.value = { ...data };
};

const closeModal = () => {
  showModal.value = false;
};

const fetchSchools = async () => {
  const res = await axios.get(`${API}/admin/schools`);
  schoolsList.value = res.data;
};

// Add School
const addSchool = async () => {
  try {
    await axios.post(`${API}/admin/schools`, schoolForm.value);
    await fetchSchools();
    emit("toast", { message: "School added successfully!", type: "success" });
    closeModal();
  } catch (err) {
    emit("toast", {
      message: err.response?.data?.error || "Error adding school",
      type: "error",
    });
  }
};

// Update School
const updateSchool = async () => {
  try {
    await axios.put(
      `${API}/admin/schools/${schoolForm.value.School_Id}`,
      schoolForm.value
    );
    await fetchSchools();
    emit("toast", { message: "School updated successfully!", type: "success" });
    closeModal();
  } catch (err) {
    emit("toast", {
      message: err.response?.data?.error || "Error updating school",
      type: "error",
    });
  }
};

// Disable/Enable School
const toggleSchoolStatus = async (school) => {
  const action = school.Is_Active ? "disable" : "enable";

  try {
    await axios.put(
      `${API}/admin/schools/toggle-status/${school.School_Id}`
    );

    await fetchSchools();

    emit("toast", {
      message: `School ${action}d successfully`,
      type: "success"
    });
  } catch (err) {
    emit("toast", {
      message: "Failed to update school status",
      type: "error"
    });
  }
};


onMounted(() => {
  fetchSchools();
});
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
