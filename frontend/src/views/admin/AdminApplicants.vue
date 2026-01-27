<template>
  <div class="space-y-6">

    <!-- Action Buttons -->
    <div class="flex gap-4 mb-6">
      <button
        @click="showAddApplicantPage = true"
        class="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all hover:scale-105"
      >
        Add Applicant
      </button>
      <button
        @click="navigateUpload"
        class="bg-purple-500 hover:bg-purple-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all hover:scale-105"
      >
        Upload Applicants
      </button>
    </div>

    <!-- Add Applicant Page -->
    <AddApplicantsPage
      v-if="showAddApplicantPage"
      @close="showAddApplicantPage = false"
      @saved="handleApplicantSaved"
    />


    <!-- Applicants Table -->
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
              <th class="py-4 px-6">#</th>
              <th class="py-4 px-6">Name</th>
              <th class="py-4 px-6">Email</th>
              <th class="py-4 px-6">Phone</th>
              <th class="py-4 px-6">Gender</th>
              <th class="py-4 px-6">Reg. Date</th>
              <th class="py-4 px-6">Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="(a, i) in applicantsList"
              :key="a.Applicant_Id"
              class="border-t hover:bg-gray-50"
            >
              <td class="px-6 py-4">
                <input
                  type="checkbox"
                  :value="a.Applicant_Id"
                  v-model="selectedApplicants"
                />
              </td>
              <td class="px-6 py-4">{{ i + 1 }}</td>
              <td class="px-6 py-4">{{ a.Full_Name }}</td>
              <td class="px-6 py-4">{{ a.Email }}</td>
              <td class="px-6 py-4">{{ a.Phone }}</td>
              <td class="px-6 py-4">{{ a.Gender }}</td>
              <td class="px-6 py-4">{{ formatDate(a.Registration_Date) }}</td>
              <td class="px-6 py-4 space-x-2">
                <button
                  @click="openViewModal(a)"
                  class="bg-blue-500 text-white px-4 py-2 rounded"
                >
                  View
                </button>
                <button
                  @click="deleteApplicant(a.Applicant_Id)"
                  class="bg-red-500 text-white px-4 py-2 rounded"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="!applicantsList.length" class="text-center py-10 text-gray-500">
        No applicants found
      </div>
    </div>

    <!-- View Modal -->
    <div
      v-if="showViewModal"
      class="fixed inset-0 bg-black/60 flex items-center justify-center z-50"
    >
      <div class="bg-white p-8 rounded-xl w-full max-w-md">
        <h3 class="text-xl font-bold mb-4">Applicant Details</h3>

        <p><b>Name:</b> {{ selectedApplicant.Full_Name }}</p>
        <p><b>Email:</b> {{ selectedApplicant.Email }}</p>
        <p><b>Phone:</b> {{ selectedApplicant.Phone }}</p>
        <p><b>Gender:</b> {{ selectedApplicant.Gender }}</p>
        <p><b>Address:</b> {{ selectedApplicant.Address }}</p>

        <div class="text-center mt-6">
          <button
            @click="showViewModal = false"
            class="px-6 py-2 bg-gray-300 rounded"
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
import { useRouter } from "vue-router";
import axios from "@/utils/axiosInstance";

const emit = defineEmits(["toast"]);
const router = useRouter();

const applicantsList = ref([]);
const selectedApplicants = ref([]);
const showViewModal = ref(false);
const selectedApplicant = ref(null);
const showAddApplicantPage = ref(false);

// ✅ FETCH
const fetchApplicants = async () => {
  const res = await axios.get("/admin/applicants");
  applicantsList.value = res.data.applicants || res.data;
};

const handleApplicantSaved = () => {
  fetchApplicants();
  emit("toast", { message: "Applicant added", type: "success" });
};

// ✅ REDIRECT (FIXED)
const goToAddApplicant = () => {
  router.push({ name: "AddApplicant" });
};

// View
const openViewModal = (a) => {
  selectedApplicant.value = a;
  showViewModal.value = true;
};

// Delete
const deleteApplicant = async (id) => {
  if (!confirm("Delete applicant?")) return;
  await axios.delete(`/admin/applicants/${id}`);
  emit("toast", { message: "Applicant deleted", type: "success" });
  fetchApplicants();
};

const toggleAll = () => {
  selectedApplicants.value =
    selectedApplicants.value.length === applicantsList.value.length
      ? []
      : applicantsList.value.map(a => a.Applicant_Id);
};

const formatDate = (d) =>
  d ? new Date(d).toLocaleDateString("en-IN") : "N/A";

const navigateUpload = () => router.push("/upload-students");

onMounted(fetchApplicants);
</script>
