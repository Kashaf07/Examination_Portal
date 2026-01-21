<template>
  <div class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-200">
    <div class="overflow-x-auto">
      <table class="w-full">
        <thead class="bg-gradient-to-r from-blue-50 to-blue-100">
          <tr>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">ID</th>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">School Name</th>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">Short Name</th>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">Actions</th>
          </tr>
        </thead>

        <tbody class="bg-white divide-y divide-gray-100">
          <tr
            v-for="(school, idx) in schoolList"
            :key="school.School_Id"
            class="hover:bg-gray-50 transition"
          >
            <td class="py-4 px-6 text-gray-900">{{ idx + 1 }}</td>
            <td class="py-4 px-6 text-gray-900">{{ school.School_Name }}</td>
            <td class="py-4 px-6 text-gray-900">{{ school.School_Short }}</td>

            <td class="py-4 px-6">
              <div class="flex gap-2">
                <button
                  @click="$emit('edit', school)"
                  class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm 
                         shadow transition hover:scale-105"
                >
                  Edit
                </button>

                <button
                  @click="$emit('delete', school.School_Id)"
                  class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm 
                         shadow transition hover:scale-105"
                >
                  Delete
                </button>
              </div>
            </td>
          </tr>

          <tr v-if="schoolList.length === 0">
            <td colspan="4" class="text-center py-6 text-gray-500">
              No schools found.
            </td>
          </tr>

        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
defineProps({
  schoolList: {
    type: Array,
    required: true
  }
});
</script>
