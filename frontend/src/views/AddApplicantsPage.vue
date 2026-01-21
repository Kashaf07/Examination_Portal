<template>
  <div class="p-6 max-w-2xl mx-auto">
    <h2 class="text-2xl font-bold mb-6">Add Applicant</h2>

    <form @submit.prevent="submitApplicant" class="space-y-4">

      <div>
        <label class="block font-semibold">Full Name</label>
        <input v-model="applicant.Full_Name" required class="w-full border px-3 py-2 rounded" />
      </div>

      <div>
        <label class="block font-semibold">Email</label>
        <input v-model="applicant.Email" type="email" required class="w-full border px-3 py-2 rounded" />
      </div>

      <div>
        <label class="block font-semibold">Password</label>
        <input v-model="applicant.Password" type="password" required class="w-full border px-3 py-2 rounded" />
      </div>

      <div>
        <label class="block font-semibold">Phone</label>
        <input v-model="applicant.Phone" class="w-full border px-3 py-2 rounded" />
      </div>

      <div>
        <label class="block font-semibold">DOB</label>
        <input v-model="applicant.DOB" type="date" class="w-full border px-3 py-2 rounded" />
      </div>

      <div>
        <label class="block font-semibold">Gender</label>
        <select v-model="applicant.Gender" class="w-full border px-3 py-2 rounded">
          <option value="">Select</option>
          <option>Male</option>
          <option>Female</option>
          <option>Other</option>
        </select>
      </div>

      <div>
        <label class="block font-semibold">Address</label>
        <textarea v-model="applicant.Address" class="w-full border px-3 py-2 rounded"></textarea>
      </div>

      <!-- ✅ GROUP DROPDOWN -->
      <div>
        <label class="block font-semibold">Group</label>
        <select v-model="applicant.group_id" required class="w-full border px-3 py-2 rounded">
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

      <button
        type="submit"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Save Applicant
      </button>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import axios from '../utils/axiosInstance'

const facultyEmail = localStorage.getItem('faculty_email')

const applicant = reactive({
  Full_Name: '',
  Email: '',
  Password: '',
  Phone: '',
  DOB: '',
  Gender: '',
  Address: '',
  group_id: ''
})

const groups = ref([])

/* -------------------------------
   LOAD GROUPS (FACULTY-WISE)
-------------------------------- */
const loadGroups = async () => {
  try {
    const res = await axios.get(`/groups/${facultyEmail}`)
    if (res.data.success) {
      groups.value = res.data.groups
    }
  } catch (err) {
    console.error('Failed to load groups', err)
  }
}

/* -------------------------------
   SUBMIT APPLICANT
-------------------------------- */
const submitApplicant = async () => {
  try {
    await axios.post('/applicants/add', applicant)
    alert('Applicant added successfully')

    Object.keys(applicant).forEach(k => applicant[k] = '')
  } catch (err) {
    console.error(err)
    alert('Error adding applicant')
  }
}

onMounted(loadGroups)
</script>
