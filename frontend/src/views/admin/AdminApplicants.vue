<template>
  <div class="space-y-6">

    <!-- Action Buttons -->
    <div class="flex gap-4 mb-6">
      <button @click="toggleAddApplicant"
        class="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all hover:scale-105"
      >
        {{ showAddApplicantPage ? 'Close' : 'Add Applicant' }}
      </button>
      <button
        @click="navigateUpload"
        class="bg-purple-500 hover:bg-purple-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all hover:scale-105"
      >
        Upload Students
      </button>
    </div>
    <div v-if="showAddApplicantPage" class="mb-8"></div>

    <!-- Add Applicant Page -->
    <AddApplicantsPage
      v-if="showAddApplicantPage"
      @close="showAddApplicantPage = false"
      @saved="handleApplicantSaved"
    />

    <!-- Applicants Table -->
    <div class="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden">

      <table class="w-full">
        <thead class="bg-gradient-to-r from-blue-50 to-blue-100 text-gray-700">
          <tr>
            <th class="py-4 px-6">
              <input
                type="checkbox"
                @change="toggleAll"
                :checked="selectedApplicants.length === applicantsList.length && applicantsList.length > 0"
              />
            </th>
            <th class="py-4 px-6 font-semibold">ID</th>
            <th class="py-4 px-6 font-semibold">Name</th>
            <th class="py-4 px-6 font-semibold">Email</th>
            <th class="py-4 px-6 font-semibold">Phone</th>
            <th class="py-4 px-6 font-semibold">Actions</th>
          </tr>
        </thead>

        <tbody class="divide-y divide-gray-100">
          <tr
            v-for="(a, i) in applicantsList"
            :key="a.Applicant_Id"
            class="hover:bg-blue-50 transition cursor-pointer"
          >
            <td class="px-6 py-5">
              <input type="checkbox" :value="a.Applicant_Id" v-model="selectedApplicants" />
            </td>

            <td class="px-6 py-5">{{ i + 1 }}</td>
            <td class="px-6 py-5 font-medium text-gray-800">{{ a.Full_Name }}</td>
            <td class="px-6 py-5">{{ a.Email }}</td>
            <td class="px-6 py-5">{{ a.Phone }}</td>

            <td class="px-6 py-5 flex gap-2">
              <button
                @click="openViewModal(a)"
                class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md shadow"
              >
                View
              </button>

              <button
                @click="deleteApplicant(a.Applicant_Id)"
                class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md shadow"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>

      </table>

      <div v-if="!applicantsList.length" class="text-center py-10 text-gray-500">
        No Students found
      </div>
    </div>

        
    <!-- View Modal -->
    <div
      v-if="showViewModal"
      class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 px-4"
    >
      <div
        class="bg-white/90 backdrop-blur-lg rounded-2xl shadow-2xl w-full max-w-lg p-8 relative animate-fadeIn"
      >
        <!-- Close Button -->
        <button
          @click="showViewModal = false"
          class="absolute top-4 right-4 w-8 h-8 flex items-center justify-center 
                rounded-full bg-gray-200 hover:bg-gray-300 transition"
        >
          ✕
        </button>

        <h3
          class="text-2xl font-extrabold text-blue-700 mb-6 text-center tracking-wide"
        >
          Applicant Details
        </h3>

        <div class="space-y-4 text-gray-700 text-base">
          <p><span class="font-semibold text-gray-900">Name:</span> {{ selectedApplicant.Full_Name }}</p>
          <p><span class="font-semibold text-gray-900">Email:</span> {{ selectedApplicant.Email }}</p>
          <p><span class="font-semibold text-gray-900">Phone:</span> {{ selectedApplicant.Phone }}</p>
          <p><span class="font-semibold text-gray-900">DOB:</span> {{ formatDOB(selectedApplicant.DOB) }}</p>
          <p><span class="font-semibold text-gray-900">Gender:</span> {{ selectedApplicant.Gender }}</p>
          <p><span class="font-semibold text-gray-900">Reg. Date:</span> {{ formatDate(selectedApplicant.Registration_Date) }}</p>
          <p><span class="font-semibold text-gray-900">Address:</span> {{ selectedApplicant.Address }}</p>
        </div>

        <!-- Bottom Close Button -->
        <div class="mt-8 text-center">
          <button
            @click="showViewModal = false"
            class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-3 rounded-full shadow-md transition"
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
import AddApplicantsPage from "../AddApplicantsPage.vue";

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

const toggleAddApplicant = () => {
  showAddApplicantPage.value = !showAddApplicantPage.value;
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

const formatDOB = (dob) => {
  if (!dob) return "N/A";
  const d = new Date(dob);
  return d.toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric"
  });
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

<style scooped>
@keyframes fadeIn {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.animate-fadeIn {
  animation: fadeIn 0.25s ease-out;
}
</style>
