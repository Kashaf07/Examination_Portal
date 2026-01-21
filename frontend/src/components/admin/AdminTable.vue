<template>
  <div class="bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden">

    <div class="overflow-x-auto">
      <table class="w-full">

        <!-- HEADER -->
        <thead>
          <tr class="bg-gradient-to-r from-blue-50 to-blue-100 border-b border-blue-200">
            <th class="text-left py-4 px-6 font-semibold text-blue-900">ID</th>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">Name</th>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">Email</th>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">Actions</th>
          </tr>
        </thead>

        <!-- BODY -->
        <tbody class="bg-white divide-y divide-gray-100">
          <tr
            v-for="(admin, idx) in admins"
            :key="admin.Admin_ID"
            class="hover:bg-gray-50 transition"
          >
            <td class="py-4 px-6 text-gray-700 font-medium">
              {{ idx + 1 }}
            </td>

            <td class="py-4 px-6 text-gray-700">
              {{ admin.Name }}
            </td>

            <td class="py-4 px-6 text-gray-700">
              {{ admin.Email }}
            </td>

            <td class="py-4 px-6 space-x-2">

              <!-- Edit -->
              <button
                @click="$emit('edit', admin)"
                class="
                  bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm 
                  font-medium transition hover:scale-105 shadow-md
                "
              >
                Edit
              </button>

              <!-- Delete -->
              <button
                @click="$emit('delete', admin.Admin_ID)"
                class="
                  bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm
                  font-medium transition hover:scale-105 shadow-md
                "
              >
                Delete
              </button>

            </td>
          </tr>
        </tbody>

      </table>
    </div>

    <!-- EMPTY STATE -->
    <div
      v-if="admins.length === 0"
      class="text-center py-10 text-gray-500"
    >
      No admins found.
    </div>

  </div>
</template>

<script setup>
const props = defineProps({
  admins: { type: Array, required: true },
});

const emit = defineEmits(["edit", "delete"]);
</script>
