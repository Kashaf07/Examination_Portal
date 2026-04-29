<template>
  <!-- Enhanced Card UI with Gemini Style -->
  <div class="max-w-4xl mx-auto bg-white rounded-2xl shadow-xl p-8 relative overflow-hidden">
    
    <!-- Gemini Icon in Corner (No Animation) -->
    <div class="absolute top-6 right-6">
      <img 
        src="/Gemini.png" 
        alt="Gemini AI" 
        class="w-12 h-12"
      />
    </div>

    <h2 class="text-3xl font-bold text-gray-800 mb-8">
      Generate Questions with AI
    </h2>

    <!-- Form -->
    <div class="space-y-5 mb-6">
      <div>
        <label class="block text-sm font-semibold text-gray-700 mb-2">Subject</label>
        <input
          v-model="subject"
          placeholder="e.g. Mathematics"
          class="w-full border-2 border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-purple-400 transition-colors"
        />
      </div>

      <div>
        <label class="block text-sm font-semibold text-gray-700 mb-2">Topics</label>
        <input
          v-model="topics"
          placeholder="e.g. Algebra, Geometry"
          class="w-full border-2 border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-purple-400 transition-colors"
        />
      </div>

      <div class="grid grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">Number of Questions</label>
          <input
            v-model="num_questions"
            type="number"
            min="1"
            max="20"
            class="w-full border-2 border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-purple-400 transition-colors"
          />
        </div>

        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">Difficulty</label>
          <select
            v-model="difficulty"
            class="w-full border-2 border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-purple-400 transition-colors"
          >
            <option>Easy</option>
            <option>Medium</option>
            <option>Hard</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">Question Type</label>
          <select
            v-model="question_type"
            class="w-full border-2 border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-purple-400 transition-colors"
          >
            <option value="MCQ">MCQ</option>
            <option value="Fill">Fill in the Blanks</option>
            <option value="One Word">One Word</option>
            <option value="True/False">True/False</option>
            <option value="Descriptive">Descriptive</option>
          </select>
        </div>
      </div>

      <!-- Generate Button - Centered and Minimal Width -->
      <div class="text-center pt-4">
        <button
          @click="generatePaper"
          :disabled="loading"
          class="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-purple-700 hover:to-blue-700 text-white font-semibold px-8 py-3 rounded-full shadow-lg transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="!loading">Generate</span>
          <span v-else class="flex items-center justify-center gap-2">
            <svg class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Generating...
          </span>
        </button>
        
        <button
          v-if="questions.length"
          @click="generateMore"
          :disabled="loading"
          class="ml-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-purple-700 hover:to-blue-700 text-white font-semibold px-8 py-3 rounded-full shadow-lg transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="!loading">+ Generate More</span>
          <span v-else>Generating...</span>
        </button>
      </div>
    </div>

    <!-- Error -->
    <p v-if="error" class="text-red-600 text-sm mb-4 bg-red-50 border border-red-200 rounded-lg p-3">
      {{ error }}
    </p>

    <!-- Generated Questions -->
    <div v-if="questions.length" class="border-t-2 border-gray-100 pt-6">
      <h3 class="font-bold text-gray-800 mb-4 text-lg">
        Generated Questions
        <span class="text-purple-600 font-semibold ml-2">({{ selectedQuestions.length }} selected)</span>
      </h3>

      <div class="space-y-3 max-h-96 overflow-y-auto pr-2 custom-scrollbar">
        <div
          v-for="(q, index) in questions"
          :key="index"
          class="border-2 rounded-xl p-4 cursor-pointer transition-all duration-200"
          :class="isSelected(q) 
            ? 'border-purple-500 bg-gradient-to-r from-purple-50 to-pink-50 shadow-md' 
            : 'border-gray-200 hover:border-purple-300 hover:shadow-sm'"
          @click="toggleSelect(q)"
        >
          <div class="flex items-start gap-3">
            <input
              type="checkbox"
              :checked="isSelected(q)"
              @click.stop="toggleSelect(q)"
              class="mt-1 w-4 h-4 accent-purple-600"
            />
            <div class="flex-1">
              <p class="font-semibold text-gray-800 text-sm mb-2">Q{{ index + 1 }}: {{ q.question }}</p>
              <div v-if="q.options" class="grid grid-cols-2 gap-2 mb-2">
                <span
                  v-for="(opt, i) in q.options"
                  :key="i"
                  class="text-xs text-gray-700 bg-gray-100 rounded-lg px-3 py-1.5 border border-gray-200"
                >
                  {{ String.fromCharCode(65 + i) }}. {{ opt }}
                </span>
              </div>
              <p class="text-xs text-green-700 font-semibold bg-green-50 inline-block px-2 py-1 rounded">
                ✓ Answer: {{ q.answer }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add to Bank Button -->
    <div v-if="selectedQuestions.length" class="mt-6 pt-4 border-t-2 border-gray-100">
      <button
        @click="addToBank"
        :disabled="saving"
        class="w-full bg-gradient-to-r from-green-500 to-emerald-600 text-white font-bold py-4 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-[1.01] active:scale-[0.99]"
      >
        {{ saving ? 'Saving...' : `✓ Add ${selectedQuestions.length} Question(s) to Bank` }}
      </button>
      <p v-if="successMsg" class="text-green-600 text-sm text-center mt-3 font-semibold bg-green-50 py-2 rounded-lg">
        {{ successMsg }}
      </p>
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
      
      // Validation
      if (!this.subject.trim() || !this.topics.trim()) {
        this.error = 'Please fill in Subject and Topics fields.';
        this.loading = false;
        return;
      }
      
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
        console.error('Generation error:', e);
        const errorMsg = e.response?.data?.error || e.message;
        this.error = `Error: ${errorMsg}`;
      }
      this.loading = false;
    },

    async generateMore() {
      this.loading = true;
      this.error = '';
      
      // Validation
      if (!this.subject.trim() || !this.topics.trim()) {
        this.error = 'Please fill in Subject and Topics fields.';
        this.loading = false;
        return;
      }
      
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
        console.error('Generation error:', e);
        const errorMsg = e.response?.data?.error || e.message;
        this.error = `Error: ${errorMsg}`;
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

<style scoped>
/* Custom scrollbar */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: linear-gradient(to bottom, #a855f7, #ec4899);
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(to bottom, #9333ea, #db2777);
}
</style>
