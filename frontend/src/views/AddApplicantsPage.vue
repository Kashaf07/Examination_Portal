<template>
  <div
    class="bg-white/80 backdrop-blur-lg shadow-xl border border-white/40
           rounded-2xl p-10 max-w-5xl mx-auto mb-10 transition-all"
  >
    <!-- ── Success Toast ── -->
    <transition name="fade">
      <div
        v-if="successMsg"
        class="flex items-center gap-3 mb-6 px-4 py-3 rounded-xl text-sm font-semibold"
        style="background:#f0fdf4; border:1px solid #bbf7d0; color:#166534;"
      >
        <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="#16a34a" stroke-width="2.5"
          stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="10"/>
          <polyline points="9 12 11 14 15 10"/>
        </svg>
        {{ successMsg }}
      </div>
    </transition>

    <!-- ── Error Toast ── -->
    <transition name="fade">
      <div
        v-if="globalError"
        class="flex items-center gap-3 mb-6 px-4 py-3 rounded-xl text-sm font-semibold"
        style="background:#fff5f5; border:1px solid #fecaca; color:#991b1b;"
      >
        <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="#dc2626" stroke-width="2.5"
          stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="10"/>
          <line x1="12" y1="8" x2="12" y2="12"/>
          <line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        {{ globalError }}
      </div>
    </transition>

    <h3 class="text-2xl font-bold mb-6 text-gray-800">Add New Student</h3>

    <form @submit.prevent="submitApplicant" class="space-y-4">
      <div class="grid grid-cols-2 gap-4">

        <!-- Full Name -->
        <div class="flex flex-col gap-1">
          <label class="font-semibold text-gray-700 text-sm">Full Name</label>
          <input v-model="applicant.Full_Name" type="text" class="input-field" />
          <p v-if="errors.Full_Name" class="error-text">{{ errors.Full_Name }}</p>
        </div>

        <!-- Email -->
        <div class="flex flex-col gap-1">
          <label class="font-semibold text-gray-700 text-sm">Email</label>
          <input v-model="applicant.Email" type="email" class="input-field" />
          <p v-if="errors.Email" class="error-text">{{ errors.Email }}</p>
        </div>

        <!-- Password -->
        <div class="flex flex-col gap-1">
          <label class="font-semibold text-gray-700 text-sm">Password</label>
          <input v-model="applicant.Password" type="password" class="input-field" />
          <p v-if="errors.Password" class="error-text">{{ errors.Password }}</p>
        </div>

        <!-- Phone -->
        <div class="flex flex-col gap-1">
          <label class="font-semibold text-gray-700 text-sm">Phone</label>
          <input v-model="applicant.Phone" type="text" class="input-field" />
          <p v-if="errors.Phone" class="error-text">{{ errors.Phone }}</p>
        </div>

        <!-- DOB -->
        <div class="flex flex-col gap-1">
          <label class="font-semibold text-gray-700 text-sm">DOB</label>
          <input v-model="applicant.DOB" type="date" class="input-field" />
          <p v-if="errors.DOB" class="error-text">{{ errors.DOB }}</p>
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
          <p v-if="errors.Gender" class="error-text">{{ errors.Gender }}</p>
        </div>

        <!-- Address -->
        <div class="flex flex-col gap-1">
          <label class="font-semibold text-gray-700 text-sm">Address</label>
          <textarea v-model="applicant.Address" rows="2" class="input-field"></textarea>
          <p v-if="errors.Address" class="error-text">{{ errors.Address }}</p>
        </div>

        <!-- Group -->
        <div class="flex flex-col gap-1">
          <label class="font-semibold text-gray-700 text-sm">Group</label>
          <select v-model="applicant.group_id" class="input-field">
            <option value="">Select Group</option>
            <option v-for="g in groups" :key="g.Group_Id" :value="g.Group_Id">
              {{ g.Group_Name }}
            </option>
          </select>
          <p v-if="errors.group_id" class="error-text">{{ errors.group_id }}</p>
        </div>

      </div>

      <!-- Buttons -->
      <div class="flex justify-end gap-3 pt-4">
        <button type="button" @click="clearForm" class="cancel-btn" :disabled="submitting">
          Clear
        </button>
        <button type="submit" class="submit-btn" :disabled="submitting">
          <span v-if="submitting" class="flex items-center gap-2">
            <svg class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="white" stroke-width="4"/>
              <path class="opacity-75" fill="white" d="M4 12a8 8 0 018-8v8z"/>
            </svg>
            Saving...
          </span>
          <span v-else>Save Applicant</span>
        </button>
      </div>

    </form>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import axios from "../utils/axiosInstance"

const router    = useRouter()
const emit      = defineEmits(["saved", "close"])

/* ── State ── */
const submitting  = ref(false)
const successMsg  = ref("")
const globalError = ref("")

/* ── Form Data ── */
const applicant = reactive({
  Full_Name: "", Email: "", Password: "",
  Phone: "", DOB: "", Gender: "", Address: "", group_id: ""
})

/* ── Errors ── */
const errors = reactive({
  Full_Name: "", Email: "", Password: "",
  Phone: "", DOB: "", Gender: "", Address: "", group_id: ""
})

const clearErrors = () => Object.keys(errors).forEach(k => (errors[k] = ""))

/* ── Toast helpers ── */
const showSuccess = (msg) => {
  globalError.value = ""
  successMsg.value  = msg
  setTimeout(() => (successMsg.value = ""), 3000)
}

const showError = (msg) => {
  successMsg.value  = ""
  globalError.value = msg
  setTimeout(() => (globalError.value = ""), 4000)
}

/* ── Groups ── */
const groups     = ref([])
const activeRole = localStorage.getItem("active_role")
const email      = localStorage.getItem("email")

const loadGroups = async () => {
  try {
    const res = await axios.get("/groups", { params: { role: activeRole, email } })
    if (res.data.success) groups.value = res.data.groups
  } catch {
    showError("Failed to load groups. Please refresh.")
  }
}

/* ── Validation ── */
const validate = () => {
  clearErrors()
  let valid = true

  if (!applicant.Full_Name) { errors.Full_Name = "Full name is required"; valid = false }

  if (!applicant.Email) { errors.Email = "Email is required"; valid = false }
  else if (!/^\S+@\S+\.\S+$/.test(applicant.Email)) { errors.Email = "Invalid email format"; valid = false }

  if (!applicant.Password) { errors.Password = "Password is required"; valid = false }
  else if (applicant.Password.length < 6) { errors.Password = "Password must be at least 6 characters"; valid = false }

  if (!applicant.Phone) { errors.Phone = "Phone number is required"; valid = false }
  else if (!/^\d{10}$/.test(applicant.Phone)) { errors.Phone = "Phone number must be 10 digits"; valid = false }

  if (!applicant.DOB)      { errors.DOB      = "Date of birth is required"; valid = false }
  if (!applicant.Gender)   { errors.Gender   = "Please select gender"; valid = false }
  if (!applicant.Address)  { errors.Address  = "Address is required"; valid = false }
  if (!applicant.group_id) { errors.group_id = "Please select a group"; valid = false }

  return valid
}

/* ── Submit ── */
const submitApplicant = async () => {
  if (!validate()) return

  submitting.value = true
  try {
    const res = await axios.post("/applicants/add", applicant)

    if (res.data.success) {
      showSuccess("Student added successfully!")
      clearForm()

      // ✅ Notify parent to refresh list
      emit("saved")

      // ✅ Close form after short delay so user sees the success message
      setTimeout(() => {
        emit("close")
        router.push(activeRole === "Admin" ? "/admin/applicants" : "/faculty")
      }, 1500)
    }
  } catch (err) {
    const data = err.response?.data
    if (data?.field) {
      // Field-level error from backend → show under the field
      errors[data.field] = data.message
    } else {
      showError(data?.message || "Something went wrong. Please try again.")
    }
  } finally {
    submitting.value = false
  }
}

/* ── Clear Form ── */
const clearForm = () => {
  Object.keys(applicant).forEach(k => (applicant[k] = ""))
  clearErrors()
  globalError.value = ""
}

onMounted(loadGroups)
</script>

<style scoped>
.input-field {
  width: 100%;
  border: 1px solid #d1d5db;
  padding: 10px 14px;
  border-radius: 12px;
  outline: none;
  transition: border-color 0.2s;
}
.input-field:focus {
  border-color: #7c3aed;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
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
  transition: background 0.2s;
}
.cancel-btn:hover:not(:disabled) { background: #d1d5db; }
.cancel-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.submit-btn {
  background: linear-gradient(to right, #2563eb, #4f46e5);
  color: white;
  padding: 0.6rem 1.5rem;
  border-radius: 12px;
  font-weight: 600;
  transition: opacity 0.2s;
  min-width: 130px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.submit-btn:hover:not(:disabled) { opacity: 0.9; }
.submit-btn:disabled { opacity: 0.6; cursor: not-allowed; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s, transform 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(-6px); }
</style>