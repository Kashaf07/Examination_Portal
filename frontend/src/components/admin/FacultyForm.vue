<template>
  <form @submit.prevent="submitForm" class="space-y-4">

    <!-- Name -->
    <div>
      <label class="block text-sm font-semibold text-gray-700 mb-2">Name</label>
      <input
        v-model="localForm.F_Name"
        type="text"
        required
        class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 
               focus:ring-blue-500 transition bg-purple-50 focus:bg-white"
      />
    </div>

    <!-- Email -->
    <div>
      <label class="block text-sm font-semibold text-gray-700 mb-2">Email</label>
      <input
        v-model="localForm.F_Email"
        type="email"
        required
        class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 
               focus:ring-blue-500 transition bg-purple-50 focus:bg-white"
      />
    </div>

    <!-- School -->
    <div>
      <label class="block text-sm font-semibold text-gray-700 mb-2">School</label>
      <select
        v-model="localForm.School_Id"
        required
        class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 
               focus:ring-blue-500 transition bg-purple-50 focus:bg-white"
      >
        <option value="">Select School</option>
        <option
          v-for="s in schools"
          :key="s.School_Id"
          :value="s.School_Id"
        >
          {{ s.School_Name }}
        </option>
      </select>
    </div>

    <!-- Designation -->
    <div>
      <label class="block text-sm font-semibold text-gray-700 mb-2">Designation</label>
      <input
        v-model="localForm.Designation"
        type="text"
        required
        class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 
               focus:ring-blue-500 transition bg-purple-50 focus:bg-white"
      />
    </div>

    <!-- Password (only for Add) -->
    <div v-if="!isEdit">
      <label class="block text-sm font-semibold text-gray-700 mb-2">Password</label>
      <input
        v-model="localForm.Password"
        type="password"
        required
        class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 
               focus:ring-blue-500 transition bg-purple-50 focus:bg-white"
      />
    </div>

    <!-- Buttons -->
    <div class="flex justify-center gap-4 pt-4">
      <button
        type="button"
        @click="$emit('cancel')"
        class="px-8 py-3 bg-gray-200 text-gray-700 rounded-full hover:bg-gray-300 
               transition hover:scale-105"
      >
        Cancel
      </button>

      <button
        type="submit"
        class="px-8 py-3 bg-blue-600 text-white rounded-full hover:bg-blue-700 
               transition hover:scale-105"
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
  schools: { type: Array, required: true },
  isEdit: { type: Boolean, default: false }
});

const emit = defineEmits(["submit", "cancel"]);

// local copy to avoid mutating parent before submit
const localForm = reactive({ ...props.form });

// Watch for parent updates when editing
watch(
  () => props.form,
  (newVal) => {
    Object.assign(localForm, newVal);
  }
);

const submitForm = () => {
  emit("submit", { ...localForm });
};
</script>
