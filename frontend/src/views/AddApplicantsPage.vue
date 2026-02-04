<template>
  <div
    class="bg-white/80 backdrop-blur-lg shadow-xl border border-white/40
           rounded-2xl p-10 max-w-5xl mx-auto mb-10 transition-all"
  >
    <h3 class="text-2xl font-bold mb-6 text-gray-800">
      Add New Student
    </h3>

    <form @submit.prevent="submitApplicant" class="space-y-4">

      <div class="grid grid-cols-2 gap-4">

        <!-- Full Name -->
        <div class="flex flex-col gap-1">
          <label class="font-semibold text-gray-700 text-sm">Full Name</label>
          <input v-model="applicant.Full_Name" type="text" class="input-field" />
          <p v-if="errors.Full_Name" class="error-text">
            {{ errors.Full_Name }}
          </p>
        </div>

        <!-- Email -->
        <div class="flex flex-col gap-1">
          <label class="font-semibold text-gray-700 text-sm">Email</label>
          <input v-model="applicant.Email" type="email" class="input-field" />
          <p v-if="errors.Email" class="error-text">
            {{ errors.Email }}
          </p>
        </div>

        <!-- Password -->
        <div class="flex flex-col gap-1">
          <label class="font-semibold text-gray-700 text-sm">Password</label>
          <input v-model="applicant.Password" type="password" class="input-field" />
          <p v-if="errors.Password" class="error-text">
            {{ errors.Password }}
          </p>
        </div>

        <!-- Phone -->
        <div class="flex flex-col gap-1">
          <label class="font-semibold text-gray-700 text-sm">Phone</label>
          <input v-model="applicant.Phone" type="text" class="input-field" />
          <p v-if="errors.Phone" class="error-text">
            {{ errors.Phone }}
          </p>
        </div>

        <!-- DOB -->
        <div class="flex flex-col gap-1">
          <label class="font-semibold text-gray-700 text-sm">DOB</label>
          <input v-model="applicant.DOB" type="date" class="input-field" />
          <p v-if="errors.DOB" class="error-text">
            {{ errors.DOB }}
          </p>
        </div>

        <!-- Gender -->
        <div class="flex flex-col gap-1">
          <label class="font-semibold text-gray-700 text-sm">Gender</label>
          <select v-model="applicant.Gender" class="input-field">
            <option value="">Select</option>
            <option>Male</option>
            <option>Female</option>
            <option>Other</option>
          </select>
          <p v-if="errors.Gender" class="error-text">
            {{ errors.Gender }}
          </p>
        </div>

        <!-- Address -->
        <div class="flex flex-col gap-1">
          <label class="font-semibold text-gray-700 text-sm">Address</label>
          <textarea
            v-model="applicant.Address"
            rows="2"
            class="input-field"
          ></textarea>
          <p v-if="errors.Address" class="error-text">
            {{ errors.Address }}
          </p>
        </div>

        <!-- Group -->
        <div class="flex flex-col gap-1">
          <label class="font-semibold text-gray-700 text-sm">Group</label>
          <select v-model="applicant.group_id" class="input-field">
            <option value="">Select Group</option>
            <option
              v-for="g in groups"
              :key="g.Group_Id"
              :value="g.Group_Id"
            >
              {{ g.Group_Name }}
            </option>
          </select>
          <p v-if="errors.group_id" class="error-text">
            {{ errors.group_id }}
          </p>
        </div>

      </div>

      <!-- Buttons -->
      <div class="flex justify-end gap-3 pt-4">
        <button type="button" @click="clearForm" class="cancel-btn">
          Clear
        </button>
        <button type="submit" class="submit-btn">
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
import NotificationToast from "@/components/admin/NotificationToast.vue"

const router = useRouter()

/* ---------------- TOAST ---------------- */
const toast = ref({ message: "", type: "" })
let toastTimer = null

const showToast = (message, type = "success") => {
  toast.value = { message, type }
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => {
    toast.value = { message: "", type: "" }
  }, 3000)
}

/* ---------------- FORM DATA ---------------- */
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

/* ---------------- ERRORS (ALL FIELDS) ---------------- */
const errors = reactive({
  Full_Name: "",
  Email: "",
  Password: "",
  Phone: "",
  DOB: "",
  Gender: "",
  Address: "",
  group_id: ""
})

const clearErrors = () => {
  Object.keys(errors).forEach(k => (errors[k] = ""))
}

/* ---------------- GROUPS ---------------- */
const groups = ref([])
const activeRole = localStorage.getItem("active_role")
const email = localStorage.getItem("email")

const loadGroups = async () => {
  const res = await axios.get("/groups", {
    params: { role: activeRole, email }
  })
  if (res.data.success) groups.value = res.data.groups
}

/* ---------------- SUBMIT ---------------- */
const submitApplicant = async () => {
  clearErrors()

  // 🔴 FRONTEND VALIDATION (ALL FIELDS)

  if (!applicant.Full_Name)
    errors.Full_Name = "Full name is required"

  if (!applicant.Email)
    errors.Email = "Email is required"
  else if (!/^\S+@\S+\.\S+$/.test(applicant.Email))
    errors.Email = "Invalid email format"

  if (!applicant.Password)
    errors.Password = "Password is required"
  else if (applicant.Password.length < 6)
    errors.Password = "Password must be at least 6 characters"

  if (!applicant.Phone)
    errors.Phone = "Phone number is required"
  else if (!/^\d{10}$/.test(applicant.Phone))
    errors.Phone = "Phone number must be 10 digits"

  if (!applicant.DOB)
    errors.DOB = "Date of birth is required"

  if (!applicant.Gender)
    errors.Gender = "Please select gender"

  if (!applicant.Address)
    errors.Address = "Address is required"

  if (!applicant.group_id)
    errors.group_id = "Please select a group"

  // ❌ STOP if any error exists
  if (Object.values(errors).some(e => e)) {
    return
  }

  // ✅ API CALL
  try {
    await axios.post("/applicants/add", applicant)
    showToast("Applicant added successfully!", "success")
    clearForm()
    router.push(activeRole === "Admin" ? "/admin/applicants" : "/faculty")
  } catch (err) {
    const data = err.response?.data
    if (data?.field) {
      errors[data.field] = data.message
    } else {
      showToast(data?.message || "Something went wrong", "error")
    }
  }
}

/* ---------------- CLEAR FORM ---------------- */
const clearForm = () => {
  Object.keys(applicant).forEach(k => (applicant[k] = ""))
  clearErrors()
}

onMounted(loadGroups)
</script>

<style scoped>
.input-field {
  width: 100%;
  border: 1px solid #d1d5db;
  padding: 10px 14px;
  border-radius: 12px;
}

.error-text {
  color: #ef4444;
  font-size: 0.75rem;
}

.cancel-btn {
  background: #e5e7eb;
  padding: 0.6rem 1.3rem;
  border-radius: 12px;
  font-weight: 600;
}

.submit-btn {
  background: linear-gradient(to right, #2563eb, #4f46e5);
  color: white;
  padding: 0.6rem 1.5rem;
  border-radius: 12px;
}
</style>
