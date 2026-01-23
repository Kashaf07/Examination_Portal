<template>
  <div class="space-y-6">

    <!-- CARD -->
    <div class="bg-white/80 backdrop-blur-sm shadow-xl rounded-2xl p-8 border border-white/20">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold text-gray-800">Designation Management</h1>
        <button 
          @click="openAddModal"
          class="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-xl font-semibold transition">
          Add Designation
        </button>
      </div>

      <!-- TABLE -->
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
              v-for="item in designations" 
              :key="item.id" 
              class="hover:bg-gray-50 transition-colors"
            >
              <td class="px-6 py-4">{{ item.id }}</td>
              <td class="px-6 py-4">{{ item.name }}</td>
              <td class="px-6 py-4 flex justify-center gap-3">

                <button
                  @click="openEditModal(item)"
                  class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-1 rounded-lg">
                  Edit
                </button>

                <button 
                  @click="deleteDesignation(item.id)"
                  class="bg-red-500 hover:bg-red-600 text-white px-4 py-1 rounded-lg">
                  Delete
                </button>

              </td>
            </tr>
          </tbody>

        </table>
      </div>
      </div>
    </div>

    <!-- ADD / EDIT MODAL -->
    <div 
      v-if="showModal"
      class="fixed inset-0 bg-black/40 flex justify-center items-center z-50"
    >
      <div class="bg-white rounded-2xl shadow-xl p-6 w-[400px]">
        
        <h2 class="text-xl font-semibold mb-4">
          {{ isEdit ? 'Edit Designation' : 'Add Designation' }}
        </h2>

        <input 
          type="text"
          v-model="modalData.name"
          class="w-full border px-3 py-2 rounded-xl"
          placeholder="Enter designation name"
        />

        <div class="flex justify-end gap-3 mt-6">
          <button 
            @click="closeModal"
            class="px-4 py-2 bg-gray-200 rounded-xl hover:bg-gray-300">
            Cancel
          </button>

          <button 
            @click="saveDesignation"
            class="px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700">
            Save
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
      modalData: {
        id: null,
        name: "",
      },
    };
  },

  mounted() {
    this.fetchDesignations();
  },

  methods: {
    async fetchDesignations() {
      const res = await axios.get("http://localhost:5000/api/admin/designations");
      this.designations = res.data.data;
    },

    openAddModal() {
      this.isEdit = false;
      this.modalData = { id: null, name: "" };
      this.showModal = true;
    },

    openEditModal(item) {
      this.isEdit = true;
      this.modalData = { id: item.id, name: item.name };
      this.showModal = true;
    },

    closeModal() {
      this.showModal = false;
    },

    async saveDesignation() { 
        try {
            let res;

            if (this.isEdit) {
                res = await axios.put(
                    `http://localhost:5000/api/admin/designations/${this.modalData.id}`,
                    { name: this.modalData.name }
                );

                this.$emit("toast", {
                    message: "Designation updated successfully!",
                    type: "success"
                });
            } else {
                // 🟢 ADD NEW DESIGNATION
                res = await axios.post(
                    "http://localhost:5000/api/admin/designations",
                    { name: this.modalData.name }
                );

                this.$emit("toast", {
                    message: "Designation added successfully!",
                    type: "success"
                });
            }
            
            this.showModal = false;
            this.fetchDesignations();
        
        } catch (err) {
            console.error("ERROR:", err.response?.data || err);
            
            // Extract error message
            const errorMsg =
            err.response?.data?.message ||
            err.response?.data?.error ||
            "Something went wrong";

            // ❗ Show error toast
            this.$emit("toast", {
                message: errorMsg,
                type: "error"    
            });
        }     
    },



    async deleteDesignation(id) {
      if (!confirm("Are you sure you want to delete this designation?")) return;

      await axios.delete(`http://localhost:5000/api/admin/designations/${id}`);
      this.fetchDesignations();
    },
  },
};
</script>
