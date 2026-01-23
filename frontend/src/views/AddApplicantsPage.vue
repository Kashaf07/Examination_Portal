<template>
  <div class="p-6 max-w-2xl mx-auto bg-white rounded-xl shadow">

    <h2 class="text-2xl font-bold mb-6 text-blue-600">
      Add Applicant
    </h2>

    <form @submit.prevent="submitApplicant" class="space-y-4">

      <!-- Full Name -->
      <div>
        <label class="block font-semibold mb-1">Full Name</label>
        <input
          v-model="applicant.Full_Name"
          required
          class="w-full border px-3 py-2 rounded"
        />
      </div>

      <!-- Email -->
      <div>
        <label class="block font-semibold mb-1">Email</label>
        <input
          v-model="applicant.Email"
          type="email"
          required
          class="w-full border px-3 py-2 rounded"
        />
      </div>

      <!-- Password -->
      <div>
        <label class="block font-semibold mb-1">Password</label>
        <input
          v-model="applicant.Password"
          type="password"
          required
          class="w-full border px-3 py-2 rounded"
        />
      </div>

      <!-- Phone -->
      <div>
        <label class="block font-semibold mb-1">Phone</label>
        <input
          v-model="applicant.Phone"
          class="w-full border px-3 py-2 rounded"
        />
      </div>

      <!-- DOB -->
      <div>
        <label class="block font-semibold mb-1">DOB</label>
        <input
          v-model="applicant.DOB"
          type="date"
          class="w-full border px-3 py-2 rounded"
        />
      </div>

      <!-- Gender -->
      <div>
        <label class="block font-semibold mb-1">Gender</label>
        <select
          v-model="applicant.Gender"
          class="w-full border px-3 py-2 rounded"
        >
          <option value="">Select</option>
          <option>Male</option>
          <option>Female</option>
          <option>Other</option>
        </select>
      </div>

      <!-- Address -->
      <div>
        <label class="block font-semibold mb-1">Address</label>
        <textarea
          v-model="applicant.Address"
          rows="3"
          class="w-full border px-3 py-2 rounded"
        ></textarea>
      </div>

      <!-- Group Dropdown -->
      <div>
        <label class="block font-semibold mb-1">Group</label>
        <select
          v-model="applicant.group_id"
          required
          class="w-full border px-3 py-2 rounded"
        >
          <option value="">Select Group</option>
          <option
            v-for="g in groups"
            :key="g.Group_Id"
            :value="g.Group_Id"
          >
            {{ g.Group_Name }}
          </option>
        </select>
      </div>

      <!-- Buttons -->
      <div class="flex justify-end gap-4 pt-4">
        <button
          type="button"
          @click="goBack"
          class="px-4 py-2 rounded bg-gray-200 hover:bg-gray-300"
        >
          Cancel
        </button>

        <button
          type="submit"
          class="px-6 py-2 rounded bg-blue-600 text-white hover:bg-blue-700"
        >
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
  router.push("/admin/applicants")
}

onMounted(loadGroups)
</script>
