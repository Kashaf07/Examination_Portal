<template>
  <div class="p-10 max-w-3xl mx-auto">
    <h2 class="text-3xl font-semibold mb-6 text-gray-800">Add Question Bank</h2>
    <p class="text-gray-600 mb-8">You are adding questions for <strong>Exam ID:</strong> {{ $route.params.examId }}</p>

    <!-- Upload Button -->
    <div class="mb-6 text-right">
      <router-link
        :to="`/exam/${$route.params.examId}/upload-question-bank`"
        class="bg-green-600 hover:bg-green-700 text-white px-5 py-2 rounded-md"
      >
        Upload CSV
      </router-link>
    </div>




    <form @submit.prevent="submitForm" class="space-y-6">
      <!-- Question Type -->
      <div>
        <label class="block font-medium mb-1 text-gray-700">Question Type</label>
        <select v-model="form.question_type" class="input-box" required>
          <option value="MCQ">MCQ</option>
          <option value="Fill">Fill in the Blanks</option>
          <option value="TF">True/False</option>
          <option value="OneWord">One Word</option>
        </select>
      </div>

      <!-- Question Text -->
      <div>
        <label class="block font-medium mb-1 text-gray-700">Question</label>
        <textarea v-model="form.question_text" class="input-box" required></textarea>
      </div>

      <!-- MCQ Options -->
      <div v-if="form.question_type === 'MCQ'" class="grid grid-cols-2 gap-4">
        <input v-model="form.option_a" placeholder="Option A" class="input-box" />
        <input v-model="form.option_b" placeholder="Option B" class="input-box" />
        <input v-model="form.option_c" placeholder="Option C" class="input-box" />
        <input v-model="form.option_d" placeholder="Option D" class="input-box" />
      </div>

      <!-- Correct Answer -->
      <div>
        <label class="block font-medium mb-1 text-gray-700">Correct Answer</label>
        <input v-model="form.correct_answer" class="input-box" required />
      </div>

      <!-- Marks -->
      <div>
        <label class="block font-medium mb-1 text-gray-700">Marks</label>
        <input v-model="form.marks" type="number" class="input-box" />
      </div>

      <!-- Submit Button -->
      <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-md">
        Submit
      </button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        exam_id: '',  // will be set in `mounted()`
        question_type: 'MCQ',
        question_text: '',
        option_a: '',
        option_b: '',
        option_c: '',
        option_d: '',
        correct_answer: '',
        marks: 1
      }
    };
  },
  methods: {
    async submitForm() {
      try {
        const response = await fetch('http://localhost:5000/api/questions/add', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.form)
        });

        const result = await response.json();

        if (response.ok) {
          alert(result.message);
          this.resetForm();
        } else {
          alert('Error: ' + result.error);
        }
      } catch (err) {
        console.error('Request failed:', err);
        alert('An error occurred.');
      }
    },
    resetForm() {
      const examId = this.$route.params.examId;
      this.form = {
        exam_id: examId,
        question_type: 'MCQ',
        question_text: '',
        option_a: '',
        option_b: '',
        option_c: '',
        option_d: '',
        correct_answer: '',
        marks: 1
      };
    },
    examList: []
  },
  mounted() {
    // ✅ Set exam_id from route param
    this.form.exam_id = this.$route.params.examId;
  }
};
</script>

<style scoped>
.input-box {
  width: 100%;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  padding: 0.5rem;
  margin-top: 0.25rem;
}
</style>
