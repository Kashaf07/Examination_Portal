<template>
  <form @submit.prevent="submitForm" class="space-y-4">

    <!-- Exam Name -->
    <div>
      <label class="block text-sm font-semibold text-gray-700 mb-2">Exam Name</label>
      <input
        v-model="localForm.exam_name"
        type="text"
        required
        placeholder="Enter exam name"
        class="w-full border border-gray-300 rounded-xl px-4 py-3
               bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- Exam Date -->
    <div>
      <label class="block text-sm font-semibold text-gray-700 mb-2">Exam Date</label>
      <input
        v-model="localForm.exam_date"
        type="date"
        required
        :min="today"
        class="w-full border border-gray-300 rounded-xl px-4 py-3
               bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- Exam Time -->
    <div>
      <label class="block text-sm font-semibold text-gray-700 mb-2">Exam Time</label>
      <input
        v-model="localForm.exam_time"
        type="time"
        required
        class="w-full border border-gray-300 rounded-xl px-4 py-3
               bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- Duration -->
    <div>
      <label class="block text-sm font-semibold text-gray-700 mb-2">Duration (Minutes)</label>
      <input
        v-model="localForm.duration"
        type="number"
        min="1"
        required
        placeholder="Enter duration in minutes"
        class="w-full border border-gray-300 rounded-xl px-4 py-3
               bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- Total Questions -->
    <div>
      <label class="block text-sm font-semibold text-gray-700 mb-2">Total Questions</label>
      <input
        v-model="localForm.total_questions"
        type="number"
        min="1"
        required
        placeholder="Enter total number of questions"
        class="w-full border border-gray-300 rounded-xl px-4 py-3
               bg-purple-50 focus:bg-white focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- Maximum Marks -->
    <div>
      <label class="block text-sm font-semibold text-gray-700 mb-2">Maximum Marks</label>
      <input
        v-model="localForm.max_marks"
        type="number"
        min="1"
        required
        placeholder="Enter maximum marks"
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
        {{ isEdit ? "Update" : "Create" }}
      </button>

    </div>

  </form>
</template>

<script setup>
import { reactive, computed, watch } from "vue";

const props = defineProps({
  form: { type: Object, required: true },
  isEdit: { type: Boolean, default: false },
});

const emit = defineEmits(["submit", "cancel"]);

const localForm = reactive({ ...props.form });

// Keep in sync when editing
watch(
  () => props.form,
  (v) => Object.assign(localForm, v)
);

// Today's date — used as min value
const today = computed(() => {
  const d = new Date();
  return d.toISOString().split("T")[0];
});

const submitForm = () => {
  emit("submit", { ...localForm });
};
</script>
