<template>
  <form @submit.prevent="submitForm" class="space-y-4">

    <!-- Name -->
    <div>
      <label class="block text-sm font-semibold text-gray-700 mb-2">Name</label>
      <input
        v-model="localForm.Name"
        type="text"
        required
        placeholder="Enter admin name"
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
        placeholder="Enter admin email"
        class="w-full border border-gray-300 rounded-xl px-4 py-3
               bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- Password (Add mode only) -->
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

// Keep synced with parent for edit mode
watch(
  () => props.form,
  (v) => Object.assign(localForm, v)
);

const submitForm = () => {
  emit("submit", { ...localForm });
};
</script>
