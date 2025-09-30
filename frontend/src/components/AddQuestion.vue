<template>
  <div class="p-10 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 rounded-2xl shadow-xl">
    <!-- Header -->
    <h2 class="text-4xl font-bold text-blue-800 mb-2 text-center">📝 Add Question Bank</h2>
    <p class="text-black-600 text-center mb-8">
      Adding questions for <strong class="text-purple-700">Exam ID: {{ $route.params.examId }}</strong>
    </p>

    <!-- Upload CSV Button -->
    <div class="mb-8 text-center">
      <router-link
        :to="`/exam/${$route.params.examId}/upload-question-bank`"
        class="p-10 max-w-4xl mx-auto bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white px-6 py-2 rounded-full shadow-md transition duration-300 ease-in-out"
      >
        📤 Upload CSV
      </router-link>
    </div>

    <!-- Add Question Form -->
    <form @submit.prevent="submitForm" class="max-w-4xl mx-auto space-y-6 bg-white p-8 rounded-xl shadow-lg">
      <!-- Question Type -->
      <div>
        <label class="block text-gray-800 font-semibold mb-2">Question Type</label>
        <select v-model="form.question_type" @change="handleTypeChange" class="input-box" required>
          <option value="MCQ">MCQ</option>
          <option value="Fill">Fill in the Blanks</option>
          <option value="TF">True/False</option>
          <option value="OneWord">One Word</option>
        </select>
      </div>

      <!-- Question Text -->
      <div>
        <label class="block text-gray-800 font-semibold mb-2">Question</label>
        <textarea v-model="form.question_text" class="input-box h-28 resize-none" required></textarea>
      </div>

      <!-- MCQ Options -->
      <div v-if="form.question_type === 'MCQ'" class="grid grid-cols-2 gap-4">
        <input v-model="form.option_a" placeholder="Option A" class="input-box" />
        <input v-model="form.option_b" placeholder="Option B" class="input-box" />
        <input v-model="form.option_c" placeholder="Option C" class="input-box" />
        <input v-model="form.option_d" placeholder="Option D" class="input-box" />
      </div>

      <!-- True/False Options (auto handled, so only show info) -->
      <div v-if="form.question_type === 'TF'" class="p-4 bg-gray-100 rounded-md text-gray-700">
        Options will be automatically set as: <br />
        <strong>Option A = True</strong>, <strong>Option B = False</strong>
      </div>

      <!-- Correct Answer -->
      <div>
        <label class="block text-gray-800 font-semibold mb-2">Correct Answer</label>
        <input 
          v-if="form.question_type !== 'TF'" 
          v-model="form.correct_answer" 
          placeholder="Enter correct answer" 
          class="input-box" 
          required 
        />
        <select 
          v-else 
          v-model="form.correct_answer" 
          class="input-box" 
          required
        >
          <option value="True">True</option>
          <option value="False">False</option>
        </select>
      </div>

      <!-- Marks -->
      <div>
        <label class="block text-gray-800 font-semibold mb-2">Marks</label>
        <input v-model="form.marks" type="number" class="input-box" />
      </div>

      <!-- Submit Button -->
      <div class="text-center pt-4">
        <button
          type="submit"
          class="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-purple-700 hover:to-blue-700 text-white font-semibold px-8 py-3 rounded-full shadow-lg transition duration-300"
        >
           Submit Question
        </button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        exam_id: '',
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
    handleTypeChange() {
      if (this.form.question_type === 'TF') {
        // Auto-set True/False options
        this.form.option_a = 'True';
        this.form.option_b = 'False';
        this.form.option_c = null;
        this.form.option_d = null;
        this.form.correct_answer = ''; // reset so faculty picks again
      } else if (this.form.question_type === 'MCQ') {
        this.form.option_a = '';
        this.form.option_b = '';
        this.form.option_c = '';
        this.form.option_d = '';
      }
    },
    async submitForm() {
      try {
        const response = await fetch('http://localhost:5000/api/questions/add', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
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
    }
  },
  mounted() {
    this.form.exam_id = this.$route.params.examId;
  }
};
</script>

