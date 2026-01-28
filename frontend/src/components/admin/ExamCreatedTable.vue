<template>
  <div class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-200">

    <div class="overflow-x-auto">
      <table class="w-full">

        <!-- HEADER -->
        <thead class="bg-gradient-to-r from-blue-50 to-blue-100">
          <tr>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">ID</th>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">Exam Name</th>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">Date</th>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">Time</th>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">Duration</th>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">Questions</th>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">Max Marks</th>
            <th class="text-left py-4 px-6 font-semibold text-blue-900">Actions</th>
          </tr>
        </thead>

        <!-- BODY -->
        <tbody class="bg-white divide-y divide-gray-100">
          <tr
            v-for="(exam, idx) in exams"
            :key="exam.Exam_Id"
            class="hover:bg-gray-50 transition"
          >
            <td class="py-4 px-6 text-gray-900">{{ idx + 1 }}</td>
            <td class="py-4 px-6 text-gray-900">{{ exam.Exam_Name }}</td>
            <td class="py-4 px-6 text-gray-900">{{ formatDate(exam.Exam_Date) }}</td>
            <td class="py-4 px-6 text-gray-900">{{ exam.Exam_Time }}</td>
            <td class="py-4 px-6 text-gray-900">{{ exam.Duration_Minutes }} min</td>
            <td class="py-4 px-6 text-gray-900">{{ exam.Total_Questions }}</td>
            <td class="py-4 px-6 text-gray-900">{{ exam.Max_Marks }}</td>

            <td class="py-4 px-6 space-x-2">

              <!-- Add Students -->
              <button
                @click="$emit('add-students', exam.Exam_Id)"
                class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1.5 rounded-lg text-xs
                       font-medium hover:scale-105 transition"
              >
                Add Students
              </button>

              <button
                            @click="navigateTo('AddQuestion', exam.Exam_Id)"
                            class="bg-green-500 text-white px-3 py-1.5 rounded-full text-xs shadow hover:scale-105 transition font-semibold"
                          >
                            Question Bank
                          </button>

                          <span
                            v-if="examStatus[exam.Exam_Id]?.has_question_bank"
                            class="text-green-600 text-lg"
                            title="Completed"
                          >
                            ✔
                          </span>
                          <span
                            v-else
                            class="text-yellow-600 text-lg"
                            title="Pending"
                          >
                            ⏳
                          </span>

                          <button
                            @click="navigateTo('MakeQuestionPaper', exam.Exam_Id)"
                            class="bg-purple-500 text-white px-3 py-1.5 rounded-full text-xs shadow hover:scale-105 transition font-semibold"
                          >
                            Question Paper
                          </button>

                          <span
                            v-if="examStatus[exam.Exam_Id]?.has_question_paper"
                            class="text-green-600 text-lg"
                            title="Completed"
                          >
                            ✔
                          </span>
                          <span
                            v-else
                            class="text-yellow-600 text-lg"
                            title="Pending"
                          >
                            ⏳
                          </span>

                          <button
                            @click="deleteExam(exam.Exam_Id)"
                            class="bg-red-500 text-white px-3 py-1.5 rounded-full text-xs shadow hover:scale-105 transition font-semibold"
                          >
                            🗑 Delete
                          </button>
                       

            </td>
          </tr>
        </tbody>

      </table>
    </div>

    <!-- EMPTY STATE -->
    <div
      v-if="exams.length === 0"
      class="text-center py-10 text-gray-500 text-sm"
    >
      No upcoming exams created yet.
    </div>

  </div>
</template>

<script setup>
const props = defineProps({
  exams: { type: Array, required: true },
});

const emit = defineEmits([
  "add-students",
  "add-question-bank",
  "make-paper",
  "delete"
]);

const formatDate = (d) => {
  if (!d) return "N/A";
  const date = new Date(d.replace(" ", "T"));
  return isNaN(date.getTime()) ? "Invalid" : date.toLocaleDateString("en-IN");
};
</script>
