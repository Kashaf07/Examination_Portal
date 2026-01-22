<template>
  <div class="space-y-6">

    <!-- Header Section -->
    <div class="bg-white/80 backdrop-blur-sm shadow-xl rounded-2xl p-8 border border-white/20">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-800">Faculty Management</h2>

        <button
          @click="openAddModal"
          class="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all hover:scale-105"
        >
          Add Faculty
        </button>
      </div>

      <!-- Faculty Table -->
      <div class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-200">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gradient-to-r from-blue-50 to-blue-100">
              <tr>
                <th class="py-4 px-6 font-semibold text-blue-900">ID</th>
                <th class="py-4 px-6 font-semibold text-blue-900">Name</th>
                <th class="py-4 px-6 font-semibold text-blue-900">Email</th>
                <th class="py-4 px-6 font-semibold text-blue-900">School</th>
                <th class="py-4 px-6 font-semibold text-blue-900">Designation</th>
                <th class="py-4 px-6 font-semibold text-blue-900">Actions</th>
              </tr>
            </thead>

            <tbody class="bg-white divide-y divide-gray-100">
              <tr
                v-for="(faculty, i) in facultyList"
                :key="faculty.Faculty_Id"
                class="hover:bg-gray-50 transition-colors"
              >
                <td class="py-4 px-6 text-gray-900">{{ i + 1 }}</td>
                <td class="py-4 px-6">{{ faculty.F_Name }}</td>
                <td class="py-4 px-6">{{ faculty.F_Email }}</td>
                <td class="py-4 px-6">{{ getSchoolName(faculty.School_Id) }}</td>
                <td class="py-4 px-6">{{ faculty.Designation }}</td>
                <td class="py-4 px-6 space-x-2">
                  <button
                    @click="openEditModal(faculty)"
                    class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm shadow transition hover:scale-105"
                  >
                    Edit
                  </button>

                  <button
                    @click="deleteFaculty(faculty.Faculty_Id)"
                    class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm shadow transition hover:scale-105"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ----------- Faculty Modal (Add/Edit) ----------- -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black/40 backdrop-blur-md flex items-center justify-center z-[1000]"
    >
      <div class="bg-white rounded-3xl shadow-2xl p-8 w-full max-w-md">
        <h3 class="text-2xl font-bold text-gray-800 mb-8 text-center">
          {{ isEdit ? "Edit Faculty" : "Add Faculty" }}
        </h3>

        <form @submit.prevent="isEdit ? updateFaculty() : addFaculty()">
          <div class="space-y-4">

            <div>
              <label class="font-semibold text-gray-700 mb-2 block">Name</label>
              <input
                v-model="facultyForm.F_Name"
                required
                class="w-full px-4 py-3 rounded-xl border border-gray-300 bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label class="font-semibold text-gray-700 mb-2 block">Email</label>
              <input
                v-model="facultyForm.F_Email"
                  type="email"
                  required
                class="w-full px-4 py-3 rounded-xl border border-gray-300 bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label class="font-semibold text-gray-700 mb-2 block">School</label>
              <select
                v-model="facultyForm.School_Id"
                required
                class="w-full px-4 py-3 rounded-xl border bg-purple-50 focus:bg-white focus:ring-2"
              >
                <option value="">Select School</option>
                <option
                  v-for="s in schoolsList"
                  :key="s.School_Id"
                  :value="s.School_Id"
                >
                  {{ s.School_Name }}
                </option>
              </select>
            </div>

            <div>
              <label class="font-semibold text-gray-700 mb-2 block">Designation</label>
              <select
                v-model="facultyForm.Designation"
                required
                class="w-full px-4 py-3 rounded-xl border bg-purple-50 focus:bg-white focus:ring-2"
              >
                <option value="">Select Designation</option>
                <option
                  v-for="d in designationsList"
                  :key="d.id"
                  :value="d.name"
                >
                  {{ d.name }}
                </option>
              </select>
            </div>


            <div v-if="!isEdit">
              <label class="font-semibold text-gray-700 mb-2 block">Password</label>
              <input
                v-model="facultyForm.Password"
                type="password"
                required
                class="w-full px-4 py-3 rounded-xl border bg-purple-50 focus:bg-white focus:ring-2"
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
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

// PARENT TOAST CONNECT
const emit = defineEmits(["toast"]);

const API = "http://localhost:5000/api";

// Data
const facultyList = ref([]);
const schoolsList = ref([]);
const designationsList = ref([]);

// Modal
const showModal = ref(false);
const isEdit = ref(false);

// Form
const facultyForm = ref({
  Faculty_Id: null,
  F_Name: "",
  F_Email: "",
  School_Id: "",
  Designation: "",
  Password: "",
});

// Open Add Modal
const openAddModal = () => {
  isEdit.value = false;
  showModal.value = true;
  facultyForm.value = {
    Faculty_Id: null,
    F_Name: "",
    F_Email: "",
    School_Id: "",
    Designation: "",
    Password: "",
  };
};

// Open Edit Modal
const openEditModal = (faculty) => {
  isEdit.value = true;
  showModal.value = true;
  facultyForm.value = {
    Faculty_Id: faculty.Faculty_Id,
    F_Name: faculty.F_Name,
    F_Email: faculty.F_Email,
    School_Id: faculty.School_Id,
    Designation: faculty.Designation,
    Password: "" // ONLY for add, ignored for update
  };
};

// Close Modal
const closeModal = () => {
  showModal.value = false
};

// Fetch Faculty
const fetchFaculty = async () => {
  const res = await axios.get(`${API}/admin/faculty`);
  facultyList.value = res.data;
};

// Fetch Schools
const fetchSchools = async () => {
  const res = await axios.get(`${API}/admin/schools`);
  schoolsList.value = res.data;
};

// Fetch Designations
const fetchDesignations = async () => {
  const res = await axios.get(`${API}/admin/designations`);
  designationsList.value = res.data.data;
};


// Get School Name
const getSchoolName = (id) => {
  const s = schoolsList.value.find((x) => x.School_Id === id);
  return s ? s.School_Name : "Unknown";
};

// Add Faculty
const addFaculty = async () => {
  try {
    await axios.post(`${API}/admin/faculty`, facultyForm.value);
    await fetchFaculty();
    emit("toast", { message: "Faculty added successfully!", type: "success" });
    closeModal();
  } catch (err) {
    emit("toast", {
      message: err.response?.data?.error || "Error adding faculty",
      type: "error",
    });
  }
};

// Update Faculty
const updateFaculty = async () => {
  try {
    await axios.put(
      `${API}/admin/faculty/${facultyForm.value.Faculty_Id}`,
      facultyForm.value
    );
    await fetchFaculty();
    emit("toast", { message: "Faculty updated successfully!", type: "success" });
    closeModal();
  } catch (err) {
    emit("toast", {
      message: err.response?.data?.error || "Error updating faculty",
      type: "error",
    });
  }
};

// Delete Faculty
const deleteFaculty = async (id) => {
  if (!confirm("Are you sure you want to delete this faculty?")) return;

  try {
    await axios.delete(`${API}/admin/faculty/${id}`);
    await fetchFaculty();
    emit("toast", { message: "Faculty deleted successfully!", type: "success" });
  } catch (err) {
    emit("toast", {
      message: err.response?.data?.error || "Error deleting faculty",
      type: "error",
    });
  }
};

onMounted(() => {
  fetchFaculty();
  fetchSchools();
  fetchDesignations();
});
</script>
