<template>
  <div>
  <!-- Info Modal (errors only) -->
  <div
    v-if="infoModal.show"
    class="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-[9999] p-4"
    @click.self="infoModal.show = false"
  >
    <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full p-8 text-center animate-fadeIn">
      <h2 class="text-2xl font-bold text-gray-800 mb-4">{{ infoModal.title }}</h2>
      <p class="text-base text-gray-600 mb-8 leading-relaxed">{{ infoModal.message }}</p>
      <button
        @click="infoModal.show = false"
        class="px-10 py-3 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-all duration-300 font-semibold shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95"
      >
        OK
      </button>
    </div>
  </div>

  <!-- Top-right Toast (success) -->
  <transition name="toast-slide">
    <div
      v-if="successToast.show"
      class="fixed right-4 z-[9999] max-w-md"
      style="top: 80px;"
    >
      <div class="p-4 rounded-xl shadow-2xl border-l-4 bg-green-50 text-green-800 border-green-500">
        <div class="flex justify-between items-center">
          <div class="flex items-center gap-3">
            <svg class="h-5 w-5 text-green-500 shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"/>
            </svg>
            <p class="text-sm font-medium">{{ successToast.message }}</p>
          </div>
          <button @click="successToast.show = false" class="text-gray-400 hover:text-gray-600 ml-4">
            <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 011.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </transition>

  <div v-if="isAuthorized" class="min-h-screen p-10 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 rounded-2xl shadow-xl">
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
  <div
  v-else
  class="min-h-screen flex items-center justify-center bg-red-50"
>
  <div class="bg-white shadow-xl rounded-xl p-8 text-center w-full max-w-md">
    
    <h2 class="text-2xl font-bold text-red-600 mb-4">
      Unauthorized Access
    </h2>

    <p class="text-gray-600 mb-6">
      You are not allowed to access this exam.
    </p>

    <!-- Go Back Button -->
    <button
  @click="$router.back()"
  class="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-lg font-semibold shadow-md transition"
>
  Go Back
</button>

  </div>
</div>
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
      isAuthorized: true,
      unauthorizedMessage: "",
      activeTab: 'add',
      infoModal: {
        show: false,
        title: '',
        message: ''
      },
      successToast: { show: false, message: '' },
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
    showInfo(title, message) {
      this.infoModal.title = title;
      this.infoModal.message = message;
      this.infoModal.show = true;
    },
    showSuccessToast(message) {
      this.successToast.message = message;
      this.successToast.show = true;
      setTimeout(() => { this.successToast.show = false; }, 3000);
    },
    async checkAuthorization() {
      try {
        const res = await fetch(
          `http://${window.location.hostname}:5000/api/questions/questionbank/all/${this.$route.params.examId}?email=${localStorage.getItem("email")}&role=${localStorage.getItem("active_role")}`
        );

        if (res.status === 403) {
          this.isAuthorized = false;
          this.unauthorizedMessage = "⚠️ Unauthorized Access";
        } else if (res.status === 404) {
          this.isAuthorized = false;
          this.unauthorizedMessage = "⚠️ Exam does not exist";
        }
      } catch (err) {
        console.error("Authorization check failed:", err);
      }
    },
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
          this.showInfo('Validation Error', 'Correct answer must be one of the MCQ options.');
          return;
        }
      }
      if (!String(this.form.correct_answer).trim()) {
        this.showInfo('Validation Error', 'Please enter the correct answer.');
        return;
      }
      try {
        const response = await fetch(`http://${window.location.hostname}:5000/api/questions/add`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            ...this.form,
            email: localStorage.getItem("email"),
            role: localStorage.getItem("active_role")
          })
        });
        const result = await response.json();
        if (response.ok) {
          this.showSuccessToast(result.message || 'Question added successfully.');
          this.resetForm();
        } else {
          this.showInfo('Error', result.error || 'Failed to add question.');
        }
      } catch (err) {
        console.error('Request failed:', err);
        this.showInfo('Error', 'An error occurred.');
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
    this.checkAuthorization();
  }
};
</script>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.95); }
  to   { opacity: 1; transform: scale(1); }
}
.animate-fadeIn {
  animation: fadeIn 0.2s ease-out;
}
.toast-slide-enter-active, .toast-slide-leave-active { transition: all 0.3s ease; }
.toast-slide-enter-from, .toast-slide-leave-to { opacity: 0; transform: translateX(60px); }
.input-box {
  width: 100%;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  padding: 0.5rem 0.75rem;
  outline: none;
  transition: border-color 0.2s;
}
.input-box:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 2px rgba(99,102,241,0.2);
}
</style>
