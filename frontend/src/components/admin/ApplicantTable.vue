<template>
  <div class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-200">
    
    <div class="overflow-x-auto">
      <table class="w-full">
        
        <!-- HEADER -->
        <thead class="bg-gradient-to-r from-blue-50 to-blue-100">
          <tr>
            <th class="py-4 px-6">
              <input
                type="checkbox"
                @change="toggleAll"
                :checked="allSelected"
              />
            </th>
            <th class="py-4 px-6 text-left font-semibold text-blue-900">ID</th>
            <th class="py-4 px-6 text-left font-semibold text-blue-900">Name</th>
            <th class="py-4 px-6 text-left font-semibold text-blue-900">Email</th>
            <th class="py-4 px-6 text-left font-semibold text-blue-900">Phone</th>
            <th class="py-4 px-6 text-left font-semibold text-blue-900">Gender</th>
            <th class="py-4 px-6 text-left font-semibold text-blue-900">Registration</th>
            <th class="py-4 px-6 text-left font-semibold text-blue-900">Actions</th>
          </tr>
        </thead>

        <!-- BODY -->
        <tbody class="bg-white divide-y divide-gray-100">
          <tr
            v-for="(a, idx) in applicants"
            :key="a.Applicant_Id"
            class="hover:bg-gray-50 transition"
          >
            <td class="py-4 px-6">
              <input
                type="checkbox"
                :value="a.Applicant_Id"
                v-model="localSelected"
                @change="emitSelection"
              />
            </td>

            <td class="py-4 px-6 text-gray-900">{{ idx + 1 }}</td>
            <td class="py-4 px-6 text-gray-900">{{ a.Full_Name }}</td>
            <td class="py-4 px-6 text-gray-900">{{ a.Email }}</td>
            <td class="py-4 px-6 text-gray-900">{{ a.Phone }}</td>
            <td class="py-4 px-6 text-gray-900">{{ a.Gender }}</td>
            <td class="py-4 px-6 text-gray-900">{{ formatDate(a.Registration_Date) }}</td>

            <td class="py-4 px-6 space-x-2">
              <button
                @click="$emit('view', a)"
                class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm hover:scale-105 transition"
              >
                View
              </button>

              <button
                @click="$emit('delete', a.Applicant_Id)"
                class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm hover:scale-105 transition"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>

      </table>
    </div>

    <!-- NO DATA -->
    <div
      v-if="applicants.length === 0"
      class="text-center py-10 text-gray-500 text-sm"
    >
      No applicants found.
    </div>

    <!-- BULK DELETE -->
    <div
      v-else
      class="flex justify-end px-6 py-4 bg-gray-50"
    >
      <button
        @click="$emit('bulk-delete')"
        :disabled="localSelected.length === 0"
        class="bg-red-500 hover:bg-red-600 disabled:bg-red-300 text-white 
               px-4 py-2 rounded-lg text-sm shadow-md disabled:cursor-not-allowed
               hover:scale-105 transition"
      >
        Delete Selected ({{ localSelected.length }})
      </button>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";

const props = defineProps({
  applicants: { type: Array, required: true },
  selected: { type: Array, default: () => [] },
});

const emit = defineEmits(["view", "delete", "bulk-delete", "toggle-selection"]);

const localSelected = ref([...props.selected]);

watch(
  () => props.selected,
  (v) => (localSelected.value = [...v])
);

const allSelected = computed(() =>
  props.applicants.length > 0 &&
  localSelected.value.length === props.applicants.length
);

const toggleAll = (e) => {
  if (e.target.checked) {
    localSelected.value = props.applicants.map((a) => a.Applicant_Id);
  } else {
    localSelected.value = [];
  }
  emitSelection();
};

const emitSelection = () => {
  emit("toggle-selection", [...localSelected.value]);
};

const formatDate = (dateString) => {
  if (!dateString) return "N/A";
  const d = new Date(dateString.replace(" ", "T"));
  return isNaN(d.getTime()) ? "Invalid" : d.toLocaleDateString("en-IN");
};
</script>
