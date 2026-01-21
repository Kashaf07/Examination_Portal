<template>
  <form @submit.prevent="submitForm" class="space-y-4">

    <!-- Full Name -->
    <div>
      <label class="block text-sm font-semibold text-gray-700 mb-2">Full Name</label>
      <input
        v-model="localForm.Full_Name"
        type="text"
        required
        placeholder="Enter full name"
        class="w-full border border-gray-300 rounded-xl px-4 py-3
               bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- Email -->
    <div>
      <label class="block text-sm font-semibold text-gray-700 mb-2">Email</label>
      <input
        v-model="localForm.Email"
        type="email"
        required
        placeholder="Enter email address"
        class="w-full border border-gray-300 rounded-xl px-4 py-3
               bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- Password (Add only) -->
    <div v-if="!isEdit">
      <label class="block text-sm font-semibold text-gray-700 mb-2">Password</label>
      <input
        v-model="localForm.Password"
        type="password"
        required
        placeholder="Enter password"
        class="w-full border border-gray-300 rounded-xl px-4 py-3
               bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- Phone -->
    <div>
      <label class="block text-sm font-semibold text-gray-700 mb-2">Phone</label>
      <input
        v-model="localForm.Phone"
        type="tel"
        placeholder="Enter phone number"
        class="w-full border border-gray-300 rounded-xl px-4 py-3
               bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- DOB -->
    <div>
      <label class="block text-sm font-semibold text-gray-700 mb-2">Date of Birth</label>
      <input
        v-model="localForm.DOB"
        type="date"
        class="w-full border border-gray-300 rounded-xl px-4 py-3
               bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- Gender -->
    <div>
      <label class="block text-sm font-semibold text-gray-700 mb-2">Gender</label>
      <select
        v-model="localForm.Gender"
        class="w-full border border-gray-300 rounded-xl px-4 py-3
               bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"
      >
        <option value="">Select Gender</option>
        <option>Male</option>
        <option>Female</option>
        <option>Other</option>
      </select>
    </div>

    <!-- Address -->
    <div>
      <label class="block text-sm font-semibold text-gray-700 mb-2">Address</label>
      <textarea
        v-model="localForm.Address"
        rows="3"
        placeholder="Enter address"
        class="w-full border border-gray-300 rounded-xl px-4 py-3
               bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"
      ></textarea>
    </div>

    <!-- Buttons -->
    <div class="flex justify-center gap-4 pt-4">
      <button
        type="button"
        @click="$emit('cancel')"
        class="px-8 py-3 bg-gray-200 text-gray-700 rounded-full
               hover:bg-gray-300 hover:scale-105 transition"
      >
        Cancel
      </button>

      <button
        type="submit"
        class="px-8 py-3 bg-blue-600 text-white rounded-full
               hover:bg-blue-700 hover:scale-105 transition"
      >
        {{ isEdit ? "Update" : "Add" }}
      </button>
    </div>

  </form>
</template>

<script setup>
import { reactive, watch } from "vue";

const props = defineProps({
  form: { type: Object, required: true },
  isEdit: { type: Boolean, default: false },
});

const emit = defineEmits(["submit", "cancel"]);

const localForm = reactive({ ...props.form });

watch(
  () => props.form,
  (v) => Object.assign(localForm, v)
);

const submitForm = () => {
  emit("submit", { ...localForm });
};
</script>
