<template>
  <div class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-200">
    <div class="overflow-x-auto">
      <table class="w-full">
        <thead class="bg-gradient-to-r from-blue-50 to-blue-100">
          <tr>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">ID</th>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">Name</th>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">Email</th>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">School</th>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">Designation</th>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">Actions</th>
          </tr>
        </thead>

        <tbody class="bg-white divide-y divide-gray-100">
          <tr
            v-for="(faculty, idx) in facultyList"
            :key="faculty.Faculty_Id"
            class="hover:bg-gray-50 transition"
          >
            <td class="py-4 px-6 text-gray-900">{{ idx + 1 }}</td>
            <td class="py-4 px-6 text-gray-900">{{ faculty.F_Name }}</td>
            <td class="py-4 px-6 text-gray-900">{{ faculty.F_Email }}</td>
            <td class="py-4 px-6 text-gray-900">{{ getSchool(faculty.School_Id) }}</td>
            <td class="py-4 px-6 text-gray-900">{{ faculty.Designation }}</td>

            <td class="py-4 px-6 space-x-2">
              <button
                @click="$emit('edit', faculty)"
                class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm shadow transition hover:scale-105"
              >
                Edit
              </button>

              <button
                @click="$emit('delete', faculty.Faculty_Id)"
                class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm shadow transition hover:scale-105"
              >
                Delete
              </button>
            </td>
          </tr>

          <tr v-if="facultyList.length === 0">
            <td colspan="6" class="text-center py-6 text-gray-500">
              No faculty found.
            </td>
          </tr>

        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  facultyList: { type: Array, required: true },
  schools: { type: Array, required: true }
});

const getSchool = (id) => {
  const found = props.schools.find((s) => s.School_Id === id);
  return found ? found.School_Name : "Unknown";
};
</script>
