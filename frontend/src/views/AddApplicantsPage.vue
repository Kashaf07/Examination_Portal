<template>
  <div :class="[
  'p mx-auto',
  'bg-white/80 backdrop-blur-lg shadow-xl border border-white/40 rounded-2xl p-10 max-w-5xl mx-auto mb-10 transition-all']">

    <h3 class="text-2xl font-bold mb-6 text-gray-800">
      Add New Applicant
    </h3>

    <form @submit.prevent="submitApplicant" class="space-y-4">

      <!-- Grid Wrapper -->
      <div class="grid grid-cols-2 gap-3">

        <!-- Full Name -->
        <div class="flex flex-col gap-1">
          <label class="font-semibold text-gray-700 text-sm">Full Name</label>
          <input v-model="applicant.Full_Name"
                required 
                type="text"
                placeholder="Enter full name"
                class="input-field"/>
        </div>

        <!-- Email -->
        <div class="flex flex-col gap-1">
          <label class="font-semibold text-gray-700 text-sm">Email</label>
          <input v-model="applicant.Email"
                type="email"
                required
                placeholder="example@mail.com"
                class="input-field"/>
        </div>

        <!-- Password -->
        <div class="flex flex-col gap-1">
          <label class="font-semibold text-gray-700 text-sm">Password</label>
          <input v-model="applicant.Password"
                type="password"
                required
                placeholder="Create password"
                class="input-field"/>
        </div>

        <!-- Phone -->
        <div class="flex flex-col gap-1">
          <label class="font-semibold text-gray-700 text-sm">Phone</label>
          <input v-model="applicant.Phone"
                type="text"
                placeholder="9876543210"
                class="input-field"/>
        </div>

        <!-- DOB -->
        <div class="flex flex-col gap-1">
          <label class="font-semibold text-gray-700 text-sm">DOB</label>
          <input v-model="applicant.DOB"
                type="date"
                class="input-field"/>
        </div>

        <!-- Gender -->
        <div class="flex flex-col gap-1">
          <label class="font-semibold text-gray-700 text-sm">Gender</label>
          <select v-model="applicant.Gender"
                  class="input-field">
            <option value="">Select</option>
            <option>Male</option>
            <option>Female</option>
            <option>Other</option>
          </select>
        </div>

      </div>

      <div class="grid grid-cols-2 gap-3">
      <!-- Address -->
      <div class="flex flex-col gap-1">
        <label class="font-semibold text-gray-700 text-sm">Address</label>
        <textarea v-model="applicant.Address"
                  rows="2"
                  placeholder="Enter address"
                  class="input-field"></textarea>
      </div>

      <!-- Group -->
      <div class="flex flex-col gap-1">
        <label class="font-semibold text-gray-700 text-sm">Group</label>
        <select v-model="applicant.group_id"
                required
                class="input-field">
          <option value="">Select Group</option>
          <option v-for="g in groups"
                  :key="g.Group_Id"
                  :value="g.Group_Id">
            {{ g.Group_Name }}
          </option>
        </select>
      </div>
      </div>

      <!-- Submit/Cancel Buttons -->
      <div class="flex justify-end gap-3 pt-2">
        <button type="button"
                @click="goBack"
                class="cancel-btn">
          Cancel
        </button>

        <button type="submit"
                class="submit-btn">
          Save Applicant
        </button>
      </div>

    </form>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import axios from "../utils/axiosInstance"

// --------------------
// ROUTER
// --------------------
const router = useRouter()

// --------------------
// AUTH DATA (FROM LOGIN)
// --------------------
const activeRole = localStorage.getItem("active_role")   // Admin / Faculty
const email = localStorage.getItem("email")

// --------------------
// FORM DATA
// --------------------
const applicant = reactive({
  Full_Name: "",
  Email: "",
  Password: "",
  Phone: "",
  DOB: "",
  Gender: "",
  Address: "",
  group_id: ""
})

// --------------------
// GROUP LIST
// --------------------
const groups = ref([])

// --------------------
// LOAD GROUPS FROM DB
// --------------------
const loadGroups = async () => {
  try {
    const res = await axios.get("/groups", {
      params: {
        role: activeRole,
        email: email
      }
    })

    if (res.data.success) {
      groups.value = res.data.groups
    }
  } catch (err) {
    console.error("LOAD GROUPS ERROR:", err.response?.data)
    alert("Failed to load groups")
  }
}

// --------------------
// SUBMIT APPLICANT
// --------------------
const submitApplicant = async () => {
  try {
    await axios.post("/applicants/add", applicant)
    alert("Applicant added successfully")

    router.push("/admin/applicants")   // redirect back
  } catch (err) {
    console.error("ADD APPLICANT ERROR:", err.response?.data)
    alert(err.response?.data?.message || "Error adding applicant")
  }
}

// --------------------
// CANCEL BUTTON
// --------------------
const goBack = () => {
  if (activeRole === "Admin") {
    router.push("/admin/applicants")
  } else {
    // Faculty mode: close this panel
    emit("closeAddApplicant")
  }
}


onMounted(loadGroups)
</script>

<style scoped>

.input-field {
  width: 100%;
  border: 1px solid #d1d5db;
  padding: 10px 14px;
  border-radius: 12px;
  background: white;
  transition: 0.2s ease;
  outline: none;
}

.input-field:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgb(59 130 246 / 25%);
}

.cancel-btn {
  background: #e5e7eb;
  padding: 0.6rem 1.3rem;
  border-radius: 12px;
  font-weight: 600;
  color: #374151;
  transition: 0.2s ease;
}

.cancel-btn:hover {
  background: #d1d5db;
}

.submit-btn {
  background: linear-gradient(to right, #2563eb, #4f46e5);
  color: white;
  padding: 0.6rem 1.5rem;
  border-radius: 12px;
  font-weight: 600;
  box-shadow: 0 2px 10px rgba(79, 70, 229, 0.2);
  transition: 0.2s ease;
}

.submit-btn:hover {
  background: linear-gradient(to right, #1d4ed8, #4338ca);
  transform: scale(1.03);
  box-shadow: 0 4px 16px rgba(79, 70, 229, 0.3);
}

</style>