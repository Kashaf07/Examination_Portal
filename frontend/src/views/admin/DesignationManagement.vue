<template>
  <div class="space-y-6">

    <!-- Header Section -->
    <div class="bg-white/80 backdrop-blur-sm shadow-xl rounded-2xl p-8 border border-white/20">

      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-800">Designation Management</h2>

        <div class="flex items-center gap-4">
          <button
            @click="openAddModal"
            class="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all hover:scale-105"
          >
            Add Designation
          </button>

          <!-- Toggle -->
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
              All Designations
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
          Disabled designations are shown in grey
        </p>
      </transition>

      <!-- Table -->
      <div class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-200">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gradient-to-r from-blue-50 to-blue-100">
              <tr>
                <th class="py-4 px-6 font-semibold text-blue-900">ID</th>
                <th class="py-4 px-6 font-semibold text-blue-900">Designation Name</th>
                <th class="py-4 px-6 font-semibold text-blue-900">Actions</th>
              </tr>
            </thead>

            <tbody class="bg-white divide-y divide-gray-100">
              <tr
                v-for="(d, i) in filteredDesignations"
                :key="d.id"
                :class="[
                  'hover:bg-gray-50 transition-colors',
                  Number(d.is_active) === 0 ? 'opacity-50 bg-gray-100' : ''
                ]"
              >
                <td class="py-4 px-6">{{ i + 1 }}</td>
                <td class="py-4 px-6">{{ d.name }}</td>

                <td class="py-4 px-6">
                  <div class="flex items-center justify-center gap-3">
                  <button
                    @click="openEditModal(d)"
                    class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm shadow transition hover:scale-105"
                  >
                    Edit
                  </button>

                  <button
                    @click="askToggleStatus(d)"
                    :class="Number(d.is_active) === 1
                      ? 'bg-red-500 hover:bg-red-600'
                      : 'bg-green-500 hover:bg-green-600'"
                    class="text-white px-4 py-2 rounded-lg text-sm shadow transition hover:scale-105"
                  >
                    {{ Number(d.is_active) === 1 ? 'Disable' : 'Enable' }}
                  </button>
                  </div>
                </td>
              </tr>
            </tbody>

          </table>
        </div>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black/60 backdrop-blur-md flex items-center justify-center z-[9999]"
    >
      <div class="bg-white shadow-2xl rounded-3xl p-8 w-full max-w-md">

        <h3 class="text-2xl font-bold text-gray-800 mb-8 text-center">
          {{ isEdit ? "Edit Designation" : "Add Designation" }}
        </h3>

        <form @submit.prevent="saveDesignation">
          <div class="space-y-4">
            <div>
              <label class="font-semibold text-gray-700 mb-2 block">
                Designation Name
              </label>
              <input
                v-model="modalData.name"
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

  <!-- Confirmation Modal for Disable/Enable Designation -->
  <div
    v-if="showConfirmModal"
    class="fixed inset-0 z-[9999] flex items-center justify-center"
  >
    <div class="absolute inset-0 bg-black/60 backdrop-blur-md"></div>

    <div class="relative bg-white/95 backdrop-blur-sm rounded-3xl shadow-2xl p-8 max-w-md w-full mx-4 transform transition-all">
      <div class="text-center">

        <h3 class="text-2xl font-bold text-gray-900 mb-3">
          {{ designationToToggle && Number(designationToToggle.is_active) === 1 ? 'Disable Designation' : 'Enable Designation' }}
        </h3>

        <p class="text-sm text-gray-600 mb-8 leading-relaxed">
          Are you sure you want to
          {{ designationToToggle && Number(designationToToggle.is_active) === 1 ? 'disable' : 'enable' }}
          this designation?
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

<script>
import axios from "axios";

export default {
  data() {
    return {
      designations: [],
      showModal: false,
      isEdit: false,
      filterMode: 'active',
      showConfirmModal: false,
      designationToToggle: null,
      modalData: {
        id: null,
        name: "",
      },
    };
  },

  computed: {
    filteredDesignations() {
      if (this.filterMode === 'active') {
        return this.designations.filter(d => Number(d.is_active) === 1);
      } else if (this.filterMode === 'inactive') {
        return this.designations.filter(d => Number(d.is_active) === 0);
      }
      return this.designations;
    },
  },

  mounted() {
    this.fetchDesignations();
  },

  methods: {
    async fetchDesignations() {
      const res = await axios.get(
        `http://${window.location.hostname}:5000/api/admin/designations`
      );
      this.designations = res.data.data;
    },

    openAddModal() {
      this.isEdit = false;
      this.modalData = { id: null, name: "" };
      this.showModal = true;
    },

    openEditModal(d) {
      this.isEdit = true;
      this.modalData = { id: d.id, name: d.name };
      this.showModal = true;
    },

    closeModal() {
      this.showModal = false;
    },

    async saveDesignation() {
      try {
        if (this.isEdit) {
          await axios.put(
            `http://${window.location.hostname}:5000/api/admin/designations/${this.modalData.id}`,
            { name: this.modalData.name }
          );
          this.$emit("toast", { message: "Designation updated!", type: "success" });
        } else {
          await axios.post(
            `http://${window.location.hostname}:5000/api/admin/designations`,
            { name: this.modalData.name }
          );
          this.$emit("toast", { message: "Designation added!", type: "success" });
        }

        this.closeModal();
        this.fetchDesignations();
      } catch (err) {
        this.$emit("toast", {
          message: err.response?.data?.message || "Operation failed",
          type: "error",
        });
      }
    },

    async toggleStatus(d) {
      const action = d.is_active ? "disable" : "enable";

      await axios.put(
        `http://${window.location.hostname}:5000/api/admin/designations/toggle-status/${d.id}`
      );

      this.$emit("toast", {
        message: `Designation ${action}d successfully`,
        type: "success",
      });

      this.fetchDesignations();
    },

    askToggleStatus(d) {
      this.designationToToggle = d;
      this.showConfirmModal = true;
    },

    cancelConfirm() {
      this.showConfirmModal = false;
      this.designationToToggle = null;
    },

    async confirmToggle() {
      const d = this.designationToToggle;
      this.showConfirmModal = false;
      this.designationToToggle = null;
      await this.toggleStatus(d);
    },
  },
};
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
