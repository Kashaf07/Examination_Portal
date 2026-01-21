<template>
  <form @submit.prevent="submitForm" class="space-y-4">

    <!-- School Name -->
    <div>
      <label class="block text-sm font-semibold text-gray-700 mb-2">
        School Name
      </label>
      <input
        v-model="localForm.School_Name"
        type="text"
        required
        placeholder="Enter School Name"
        class="w-full border border-gray-300 rounded-xl px-4 py-3
               bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- School Short Name -->
    <div>
      <label class="block text-sm font-semibold text-gray-700 mb-2">
        Short Name
      </label>
      <input
        v-model="localForm.School_Short"
        type="text"
        required
        placeholder="e.g. SOC, SCE"
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

// Local copy to avoid modifying parent before submit
const localForm = reactive({ ...props.form });

// Sync parent values when editing
watch(
  () => props.form,
  (newVal) => Object.assign(localForm, newVal)
);

const submitForm = () => {
  emit("submit", { ...localForm });
};
</script>
