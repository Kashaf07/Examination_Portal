<template>
  <div class="min-h-screen p-10 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 rounded-2xl shadow-xl">
    <!-- Back Button -->
    <button
      @click="goBack"
      class="mb-6 flex items-center gap-2 px-4 py-2 bg-white/70 hover:bg-white/90 
             text-gray-800 rounded-lg shadow-md hover:shadow-lg transition-all duration-200 
             backdrop-blur-sm border border-gray-200"
    >
      <svg 
        xmlns="http://www.w3.org/2000/svg" 
        class="h-5 w-5" 
        viewBox="0 0 20 20" 
        fill="currentColor"
      >
        <path 
          fill-rule="evenodd" 
          d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" 
          clip-rule="evenodd" 
        />
      </svg>
      <span class="font-semibold">Back</span>
    </button>
    
    <!-- Header -->
    <h2 class="text-4xl font-bold text-blue-800 mb-2 text-center">📝 Add Question Bank</h2>
    <p class="text-black-600 text-center mb-8">
      Adding questions for
      <strong class="text-purple-700">Exam ID: {{ $route.params.examId }}</strong>
    </p>

    <!-- Action Buttons (like Students page) -->
    <div class="flex gap-4 justify-center mb-8">
      <button
        @click="activeTab = 'add'"
        :class="activeTab === 'add' ? activeBtn : inactiveBtn"
      >
        ➕ Add Question
      </button>

      <button
        @click="activeTab = 'upload'"
        :class="activeTab === 'upload' ? activeBtn : inactiveBtn"
      >
        📤 Upload Questions
      </button>
    </div>

    <!-- Upload Questions -->
    <UploadQuestionBank
      v-if="activeTab === 'upload'"
      :examId="$route.params.examId"
    />

    <!-- Add Question Form -->
    <form
      v-if="activeTab === 'add'"
      @submit.prevent="submitForm"
      class="max-w-4xl mx-auto space-y-6 bg-white p-8 rounded-xl shadow-lg mt-4"
    >
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
        <input v-model="form.option_a" placeholder="Option A" class="input-box" required />
        <input v-model="form.option_b" placeholder="Option B" class="input-box" required />
        <input v-model="form.option_c" placeholder="Option C" class="input-box" required />
        <input v-model="form.option_d" placeholder="Option D" class="input-box" required />
      </div>

      <!-- True/False info -->
      <div v-if="form.question_type === 'TF'" class="p-4 bg-gray-100 rounded-md text-gray-700">
        Options will be automatically set as:
        <br />
        <strong>Option A = True</strong>, <strong>Option B = False</strong>
      </div>

      <!-- Correct Answer -->
      <div>
        <label class="block text-gray-800 font-semibold mb-2">Correct Answer</label>

        <!-- MCQ: dropdown -->
        <select
          v-if="form.question_type === 'MCQ'"
          v-model="form.correct_answer"
          class="input-box"
          required
        >
          <option disabled value="">Select Correct Answer</option>
          <option v-if="form.option_a" :value="form.option_a">{{ form.option_a }}</option>
          <option v-if="form.option_b" :value="form.option_b">{{ form.option_b }}</option>
          <option v-if="form.option_c" :value="form.option_c">{{ form.option_c }}</option>
          <option v-if="form.option_d" :value="form.option_d">{{ form.option_d }}</option>
        </select>

        <!-- TF: True/False -->
        <select
          v-else-if="form.question_type === 'TF'"
          v-model="form.correct_answer"
          class="input-box"
          required
        >
          <option value="True">True</option>
          <option value="False">False</option>
        </select>

        <!-- Others: free input -->
        <input
          v-else
          v-model="form.correct_answer"
          placeholder="Enter correct answer"
          class="input-box"
          required
        />
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
import UploadQuestionBank from '../views/UploadQuestionBank.vue';

export default {
  components: {
    UploadQuestionBank
  },
  data() {
    return {
      activeTab: 'add', // default
      activeBtn:
        'bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all hover:scale-105',
      inactiveBtn:
        'bg-gray-200 text-gray-700 px-6 py-3 rounded-full font-semibold hover:bg-gray-300 shadow-lg transition-all hover:scale-105',
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
      },
    };
  },
  methods: {
    goBack() {
      // Navigate based on active role
      const activeRole = localStorage.getItem('active_role')
      
      if (activeRole === 'Admin') {
        this.$router.push('/admin/exams')
      } else if (activeRole === 'Faculty') {
        this.$router.push('/faculty')
      } else {
        this.$router.push('/')
      }
    },
    handleTypeChange() {
      if (this.form.question_type === 'TF') {
        this.form.option_a = 'True';
        this.form.option_b = 'False';
        this.form.option_c = '';
        this.form.option_d = '';
        this.form.correct_answer = '';
      } else if (this.form.question_type === 'MCQ') {
        this.form.option_a = '';
        this.form.option_b = '';
        this.form.option_c = '';
        this.form.option_d = '';
        this.form.correct_answer = '';
      } else {
        this.form.option_a = '';
        this.form.option_b = '';
        this.form.option_c = '';
        this.form.option_d = '';
      }
    },
    async submitForm() {
      if (this.form.question_type === 'MCQ') {
        const options = [
          (this.form.option_a || '').trim(),
          (this.form.option_b || '').trim(),
          (this.form.option_c || '').trim(),
          (this.form.option_d || '').trim()
        ];
        const correct = (this.form.correct_answer || '').trim();
        if (!options.includes(correct)) {
          alert('Error: Correct answer must be one of the MCQ options.');
          return;
        }
      }
      if (!String(this.form.correct_answer).trim()) {
        alert('Error: Please enter the correct answer.');
        return;
      }
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
          alert('Error: ' + (result.error || 'Failed to add question.'));
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