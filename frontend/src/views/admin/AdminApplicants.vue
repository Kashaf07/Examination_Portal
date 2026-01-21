<template>
  <div class="space-y-6">

    <!-- Action Buttons -->
    <div class="flex gap-4 mb-6">
      <button
        @click="toggleAddForm"
        class="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all hover:scale-105"
      >
        {{ showAddForm ? "Close" : "Add Applicant" }}
      </button>

      <button
        @click="navigateUpload"
        class="bg-purple-500 hover:bg-purple-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all hover:scale-105"
      >
        Upload Applicants
      </button>
    </div>

    <!-- ----------- Add Applicant Form ----------- -->
    <div
      v-if="showAddForm"
      class="bg-white/80 backdrop-blur-sm shadow-xl rounded-2xl p-8 border border-white/20"
    >
      <h3 class="text-2xl font-bold text-gray-800 mb-6">Add New Applicant</h3>

      <form @submit.prevent="addApplicant">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">

          <CustomInput label="Full Name" v-model="newApplicant.Full_Name" required />
          <CustomInput label="Email" type="email" v-model="newApplicant.Email" required />
          <CustomInput label="Password" type="password" v-model="newApplicant.Password" required />
          <CustomInput label="Phone" v-model="newApplicant.Phone" />
          <CustomInput label="DOB" type="date" v-model="newApplicant.DOB" />

          <div>
            <label class="block text-sm font-semibold mb-2 text-gray-700">Gender</label>
            <select
              v-model="newApplicant.Gender"
              class="w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select</option>
              <option>Male</option>
              <option>Female</option>
              <option>Other</option>
            </select>
          </div>

          <div class="md:col-span-2">
            <label class="block text-sm font-semibold mb-2 text-gray-700">Address</label>
            <textarea
              v-model="newApplicant.Address"
              rows="3"
              class="w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500"
            ></textarea>
          </div>

        </div>

        <div class="flex justify-end mt-6 space-x-4">
          <button
            type="button"
            @click="showAddForm = false"
            class="px-6 py-3 rounded-full bg-gray-200 hover:bg-gray-300"
          >
            Cancel
          </button>

          <button
            type="submit"
            class="px-6 py-3 rounded-full bg-blue-500 hover:bg-blue-600 text-white"
          >
            Add Applicant
          </button>
        </div>
      </form>
    </div>

    <!-- ----------- Applicants Table ----------- -->
    <div class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-200">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gradient-to-r from-blue-50 to-blue-100">
            <tr>
              <th class="py-4 px-6">
                <input
                  type="checkbox"
                  @change="toggleAll"
                  :checked="selectedApplicants.length === applicantsList.length && applicantsList.length > 0"
                />
              </th>

              <th class="py-4 px-6 font-semibold text-blue-900">ID</th>
              <th class="py-4 px-6 font-semibold text-blue-900">Name</th>
              <th class="py-4 px-6 font-semibold text-blue-900">Email</th>
              <th class="py-4 px-6 font-semibold text-blue-900">Phone</th>
              <th class="py-4 px-6 font-semibold text-blue-900">Gender</th>
              <th class="py-4 px-6 font-semibold text-blue-900">Reg. Date</th>
              <th class="py-4 px-6 font-semibold text-blue-900">Actions</th>
            </tr>
          </thead>

          <tbody class="bg-white divide-y divide-gray-100">
            <tr
              v-for="(applicant, i) in applicantsList"
              :key="applicant.Applicant_Id"
              class="hover:bg-gray-50 transition-colors"
            >
              <td class="px-6 py-4">
                <input
                  type="checkbox"
                  :value="applicant.Applicant_Id"
                  v-model="selectedApplicants"
                />
              </td>

              <td class="px-6 py-4">{{ i + 1 }}</td>
              <td class="px-6 py-4">{{ applicant.Full_Name }}</td>
              <td class="px-6 py-4">{{ applicant.Email }}</td>
              <td class="px-6 py-4">{{ applicant.Phone }}</td>
              <td class="px-6 py-4">{{ applicant.Gender }}</td>
              <td class="px-6 py-4">{{ formatDate(applicant.Registration_Date) }}</td>

              <td class="px-6 py-4 space-x-2">
                <button
                  @click="openViewModal(applicant)"
                  class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm shadow transition hover:scale-105"
                >
                  View
                </button>

                <button
                  @click="deleteApplicant(applicant.Applicant_Id)"
                  class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm shadow transition hover:scale-105"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="applicantsList.length === 0" class="text-center py-12 text-gray-500">
        No applicants found.
      </div>

      <div v-else class="flex justify-end px-6 py-4 bg-gray-50">
        <button
          @click="deleteSelected"
          :disabled="selectedApplicants.length === 0"
          class="bg-red-500 hover:bg-red-600 disabled:opacity-50 disabled:cursor-not-allowed text-white px-4 py-2 rounded-lg text-sm shadow transition hover:scale-105"
        >
          Delete Selected ({{ selectedApplicants.length }})
        </button>
      </div>
    </div>

    <!-- ----------- View Applicant Modal ----------- -->
    <div
      v-if="showViewModal"
      class="fixed inset-0 bg-black/60 backdrop-blur-md flex items-center justify-center z-[9999]"
    >
      <div class="bg-white rounded-3xl shadow-2xl p-8 max-w-md w-full">

        <h3 class="text-2xl font-bold text-gray-800 mb-6 text-center">
          Applicant Details
        </h3>

        <div v-if="selectedApplicant" class="space-y-4">
          <DetailRow label="Name" :value="selectedApplicant.Full_Name" />
          <DetailRow label="Email" :value="selectedApplicant.Email" />
          <DetailRow label="Phone" :value="selectedApplicant.Phone" />
          <DetailRow label="DOB" :value="formatDate(selectedApplicant.DOB)" />
          <DetailRow label="Gender" :value="selectedApplicant.Gender" />
          <DetailRow label="Address" :value="selectedApplicant.Address" />
          <DetailRow label="Registration Date" :value="formatDate(selectedApplicant.Registration_Date)" />
        </div>

        <div class="flex justify-center mt-6">
          <button
            @click="showViewModal = false"
            class="px-8 py-3 rounded-full bg-gray-200 hover:bg-gray-300"
          >
            Close
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const emit = defineEmits(["toast"]);
const router = useRouter();

const DetailRow = {
  props: ["label", "value"],
  template: `
    <div class="flex justify-between py-2 border-b text-gray-700">
      <span class="font-semibold">{{ label }}:</span>
      <span>{{ value }}</span>
    </div>
  `,
};

// API
const API = "http://localhost:5000/api";

// Data
const applicantsList = ref([]);
const selectedApplicants = ref([]);
const showAddForm = ref(false);
const showViewModal = ref(false);
const selectedApplicant = ref(null);

// Add form data
const newApplicant = ref({
  Full_Name: "",
  Email: "",
  Password: "",
  Phone: "",
  DOB: "",
  Gender: "",
  Address: "",
});

// ---------- Functions ----------

// Fetch applicants
const fetchApplicants = async () => {
  const res = await axios.get(`${API}/admin/applicants`);
  applicantsList.value = res.data;
};

// Add applicant
const addApplicant = async () => {
  try {
    const res = await axios.post(`${API}/applicants/add`, newApplicant.value);

    if (res.data.success) {
      emit("toast", { message: "Applicant added successfully!", type: "success" });
      fetchApplicants();
      showAddForm.value = false;

      newApplicant.value = {
        Full_Name: "",
        Email: "",
        Password: "",
        Phone: "",
        DOB: "",
        Gender: "",
        Address: "",
      };
    } else {
      emit("toast", { message: res.data.message || "Error adding applicant", type: "error" });
    }
  } catch (err) {
    emit("toast", {
      message: err.response?.data?.error || "Error adding applicant",
      type: "error",
    });
  }
};

// Toggle all checkboxes
const toggleAll = () => {
  if (selectedApplicants.value.length === applicantsList.value.length) {
    selectedApplicants.value = [];
  } else {
    selectedApplicants.value = applicantsList.value.map(a => a.Applicant_Id);
  }
};

// Delete applicant
const deleteApplicant = async (id) => {
  if (!confirm("Delete this applicant? All logs & attempts will be deleted.")) return;

  try {
    const res = await axios.delete(`${API}/admin/applicants/${id}`);
    emit("toast", { message: res.data.message || "Applicant deleted", type: "success" });
    fetchApplicants();
  } catch (err) {
    emit("toast", {
      message: err.response?.data?.error || "Error deleting applicant",
      type: "error",
    });
  }
};

// Bulk delete
const deleteSelected = async () => {
  if (selectedApplicants.value.length === 0) return;

  if (!confirm(`Delete ${selectedApplicants.value.length} applicants?`)) return;

  try {
    await axios.post(`${API}/admin/applicants/bulk-delete`, {
      applicant_ids: selectedApplicants.value,
    });

    selectedApplicants.value = [];
    fetchApplicants();
    emit("toast", { message: "Selected applicants deleted", type: "success" });

  } catch (err) {
    emit("toast", {
      message: err.response?.data?.error || "Error deleting applicants",
      type: "error",
    });
  }
};

// Format date
const formatDate = (d) => {
  if (!d) return "N/A";
  return new Date(d).toLocaleDateString("en-IN");
};

// Open view modal
const openViewModal = (applicant) => {
  selectedApplicant.value = applicant;
  showViewModal.value = true;
};

// Navigate to upload page
const navigateUpload = () => router.push("/upload-students");

onMounted(() => {
  fetchApplicants();
});
</script>
