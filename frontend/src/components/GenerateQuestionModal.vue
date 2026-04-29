<template>
  <!-- Simple Clean Card UI -->
  <div class="max-w-4xl mx-auto bg-white rounded-xl shadow-lg p-8">
    
    <h2 class="text-2xl font-bold text-gray-800 mb-6">Generate Questions with AI</h2>

    <!-- Form -->
    <div class="space-y-4 mb-6">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Subject</label>
        <input
          v-model="subject"
          placeholder="e.g. Mathematics"
          class="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-gray-500"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Topics</label>
        <input
          v-model="topics"
          placeholder="e.g. Algebra, Geometry"
          class="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-gray-500"
        />
      </div>

      <div class="grid grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Number of Questions</label>
          <input
            v-model="num_questions"
            type="number"
            min="1"
            max="20"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-gray-500"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Difficulty</label>
          <select
            v-model="difficulty"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-gray-500"
          >
            <option>Easy</option>
            <option>Medium</option>
            <option>Hard</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Question Type</label>
          <select
            v-model="question_type"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-gray-500"
          >
            <option value="MCQ">MCQ</option>
            <option value="Fill">Fill in the Blanks</option>
            <option value="One Word">One Word</option>
            <option value="True/False">True/False</option>
            <option value="Descriptive">Descriptive</option>
          </select>
        </div>
      </div>

      <div class="flex gap-3 pt-2">
        <button
          @click="generatePaper"
          :disabled="loading"
          class="flex-1 bg-gray-800 text-white font-medium py-2 rounded-lg hover:bg-gray-900 transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ loading ? 'Generating...' : 'Generate' }}
        </button>
        <button
          v-if="questions.length"
          @click="generateMore"
          :disabled="loading"
          class="flex-1 bg-gray-600 text-white font-medium py-2 rounded-lg hover:bg-gray-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Generate More
        </button>
      </div>
    </div>

    <!-- Error -->
    <p v-if="error" class="text-red-600 text-sm mb-4">{{ error }}</p>

    <!-- Generated Questions -->
    <div v-if="questions.length" class="border-t pt-6">
      <h3 class="font-semibold text-gray-800 mb-4">
        Generated Questions
        <span class="text-gray-600 font-normal ml-2">({{ selectedQuestions.length }} selected)</span>
      </h3>

      <div class="space-y-3 max-h-96 overflow-y-auto">
        <div
          v-for="(q, index) in questions"
          :key="index"
          class="border rounded-lg p-4 cursor-pointer transition"
          :class="isSelected(q) ? 'border-gray-800 bg-gray-50' : 'border-gray-200 hover:border-gray-400'"
          @click="toggleSelect(q)"
        >
          <div class="flex items-start gap-3">
            <input
              type="checkbox"
              :checked="isSelected(q)"
              @click.stop="toggleSelect(q)"
              class="mt-1"
            />
            <div class="flex-1">
              <p class="font-medium text-gray-800 text-sm mb-2">Q{{ index + 1 }}: {{ q.question }}</p>
              <div v-if="q.options" class="grid grid-cols-2 gap-2 mb-2">
                <span
                  v-for="(opt, i) in q.options"
                  :key="i"
                  class="text-xs text-gray-600 bg-gray-100 rounded px-2 py-1"
                >
                  {{ String.fromCharCode(65 + i) }}. {{ opt }}
                </span>
              </div>
              <p class="text-xs text-green-700 font-medium">Answer: {{ q.answer }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add to Bank Button -->
    <div v-if="selectedQuestions.length" class="mt-6 pt-4 border-t">
      <button
        @click="addToBank"
        :disabled="saving"
        class="w-full bg-gray-800 text-white font-semibold py-3 rounded-lg hover:bg-gray-900 transition disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {{ saving ? 'Saving...' : `Add ${selectedQuestions.length} Question(s) to Bank` }}
      </button>
      <p v-if="successMsg" class="text-green-600 text-sm text-center mt-2 font-medium">{{ successMsg }}</p>
    </div>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    examId: { type: [String, Number], required: true }
  },
  emits: ['questions-added'],
  data() {
    return {
      subject: '',
      topics: '',
      num_questions: 5,
      difficulty: 'Medium',
      question_type: 'MCQ',
      questions: [],
      selectedQuestions: [],
      loading: false,
      saving: false,
      error: '',
      successMsg: ''
    };
  },
  methods: {
    async generatePaper() {
      this.loading = true;
      this.error = '';
      this.questions = [];
      this.selectedQuestions = [];
      try {
        const res = await axios.post(
          `http://${window.location.hostname}:5000/generate-paper`,
          {
            subject: this.subject,
            topics: this.topics,
            num_questions: this.num_questions,
            difficulty: this.difficulty,
            question_type: this.question_type
          }
        );
        if (Array.isArray(res.data)) {
          this.questions = res.data;
        } else {
          this.error = 'Failed to generate questions. Try again.';
        }
      } catch (e) {
        this.error = 'Server error. Make sure the AI backend is running.';
      }
      this.loading = false;
    },

    async generateMore() {
      this.loading = true;
      this.error = '';
      try {
        const res = await axios.post(
          `http://${window.location.hostname}:5000/generate-paper`,
          {
            subject: this.subject,
            topics: this.topics,
            num_questions: this.num_questions,
            difficulty: this.difficulty,
            question_type: this.question_type
          }
        );
        if (Array.isArray(res.data)) {
          this.questions = [...this.questions, ...res.data];
        }
      } catch (e) {
        this.error = 'Server error.';
      }
      this.loading = false;
    },

    isSelected(q) {
      return this.selectedQuestions.includes(q);
    },

    toggleSelect(q) {
      if (this.isSelected(q)) {
        this.selectedQuestions = this.selectedQuestions.filter(s => s !== q);
      } else {
        this.selectedQuestions.push(q);
      }
    },

    async addToBank() {
      this.saving = true;
      this.successMsg = '';
      try {
        const res = await fetch(
          `http://${window.location.hostname}:5000/api/questions/add-generated`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              exam_id: this.examId,
              questions: this.selectedQuestions,
              email: localStorage.getItem('email'),
              role: localStorage.getItem('active_role')
            })
          }
        );
        const result = await res.json();
        if (res.ok) {
          this.successMsg = result.message || 'Questions added!';
          this.selectedQuestions = [];
          this.questions = [];
          this.$emit('questions-added');
          setTimeout(() => {
            this.successMsg = '';
          }, 2000);
        } else {
          this.error = result.error || 'Failed to save.';
        }
      } catch (e) {
        this.error = 'Error saving questions.';
      }
      this.saving = false;
    }
  }
};
</script>
