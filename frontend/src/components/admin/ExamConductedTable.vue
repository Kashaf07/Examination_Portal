<template>
  <div
    v-if="exams.length"
    class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-200"
  >

    <!-- Title Bar -->
    <div class="px-6 py-4 bg-gradient-to-r from-purple-50 to-purple-100 border-b border-purple-200">
      <h2 class="text-2xl font-bold text-purple-900">Conducted Exams</h2>
    </div>

    <!-- Table -->
    <div class="overflow-x-auto">
      <table class="w-full">
        <thead class="bg-gradient-to-r from-blue-50 to-blue-100">
          <tr>
            <th class="py-4 px-6 text-left font-semibold text-blue-900">ID</th>
            <th class="py-4 px-6 text-left font-semibold text-blue-900">Exam Name</th>
            <th class="py-4 px-6 text-left font-semibold text-blue-900">Date</th>
            <th class="py-4 px-6 text-left font-semibold text-blue-900">Faculty Email</th>
            <th class="py-4 px-6 text-left font-semibold text-blue-900">Total Applicants</th>
            <th class="py-4 px-6 text-left font-semibold text-blue-900">Attempted</th>
            <th class="py-4 px-6 text-center font-semibold text-blue-900">Actions</th>
          </tr>
        </thead>

        <tbody class="bg-white divide-y divide-gray-100">
          <tr
            v-for="(exam, idx) in exams"
            :key="exam.Exam_Id"
            class="hover:bg-gray-50 transition"
          >
            <td class="py-4 px-6 text-gray-900">{{ idx + 1 }}</td>

            <td class="py-4 px-6 text-gray-900">
              {{ exam.Exam_Name || "N/A" }}
            </td>

            <td class="py-4 px-6 text-gray-900">
              {{ formatDate(exam.Exam_Date) }}
            </td>

            <td class="py-4 px-6 text-gray-900">
              {{ exam.faculty_email || "N/A" }}
            </td>

            <td class="py-4 px-6 text-gray-900">
              {{ exam.total_applicants || 0 }}
            </td>

            <td class="py-4 px-6 text-gray-900">
              {{ exam.attempted_applicants || 0 }}
            </td>

            <td class="py-4 px-6 text-center">
              <button
                @click="$emit('view-responses', exam.Exam_Id)"
                class="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2
                       rounded-lg text-sm shadow-md hover:scale-105 transition"
              >
                View Responses
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>

  <!-- Empty State -->
  <div
    v-else
    class="text-center py-12 text-gray-500 text-sm"
  >
    No conducted exams yet.
  </div>
</template>

<script setup>
const props = defineProps({
  exams: { type: Array, required: true },
});

const emit = defineEmits(["view-responses"]);

const formatDate = (dateString) => {
  if (!dateString) return "N/A";
  const d = new Date(dateString.replace(" ", "T"));
  return isNaN(d.getTime()) ? "Invalid" : d.toLocaleDateString("en-IN");
};
</script>
