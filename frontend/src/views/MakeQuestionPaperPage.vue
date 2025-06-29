<template>
  <div class="min-h-screen p-10 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
    
    <!-- Heading -->
    <div class="text-center mb-6">
      <h1 class="text-4xl font-bold text-blue-800 flex justify-center items-center gap-2">
        📚 Make Question Paper
      </h1>
      <p class="text-gray-700">
        Select questions for <strong class="text-purple-700">Exam ID: {{ examId }}</strong>
      </p>
    </div>

    <!-- Marks Summary -->
    <div class="bg-yellow-100 border-l-4 border-yellow-500 rounded-lg p-4 mb-8 shadow-md max-w-2xl mx-auto">
      <p class="text-lg font-semibold text-red-700">📋 Total Allowed Marks: <span class="text-blue-700">{{ examTotalMarks }}</span></p>
      <p class="text-green-700">✅ Current Total Marks: {{ currentTotalMarks }}</p>
      <p class="text-gray-800">🟢 Remaining Marks: {{ remainingMarks }}</p>
    </div>

    <!-- Question Cards -->
    <div class="space-y-4 max-w-3xl mx-auto">
      <div
        v-for="(q, index) in questions"
        :key="q.Question_Id"
        class="bg-white rounded-xl p-5 shadow hover:shadow-lg transition"
      >
        <p class="font-semibold text-lg">{{ index + 1 }}. {{ q.Question_Text }}</p>
        <p class="text-sm text-gray-600 mb-3">Marks: {{ q.Marks }}</p>
        <button
          @click="addQuestionToPaper(q)"
          :disabled="selectedQuestions.some(sq => sq.Question_Id === q.Question_Id)"
          class="flex items-center gap-2 px-4 py-2 text-white rounded-full text-sm font-medium"
          :class="selectedQuestions.some(sq => sq.Question_Id === q.Question_Id)
            ? 'bg-gray-400 cursor-not-allowed'
            : 'bg-green-500 hover:bg-green-600'"
        >
          <span v-if="selectedQuestions.some(sq => sq.Question_Id === q.Question_Id)">✅ Added</span>
          <span v-else>➕ Add to Paper</span>
        </button>
      </div>
    </div>

    <!-- 🎲 Random Button -->
    <div class="text-center mt-10">
      <button
        @click="randomizeQuestions"
        class="px-6 py-2 bg-purple-600 text-white font-semibold text-sm rounded-full hover:bg-purple-700 transition"
      >
        🎲 Randomize Questions
      </button>
    </div>

    <!-- Selected Questions -->
    <div v-if="selectedQuestions.length" class="mt-10 max-w-3xl mx-auto">
      <h2 class="text-xl font-semibold mb-4 text-blue-700">📝 Selected Questions</h2>
      <ul class="space-y-3">
        <li
          v-for="(sq, i) in selectedQuestions"
          :key="sq.Question_Id"
          class="bg-white p-4 rounded-xl shadow flex justify-between items-center"
        >
          <span>{{ i + 1 }}. {{ sq.Question_Text }} ({{ sq.Marks }} marks)</span>
          <button
            @click="removeQuestion(sq.Question_Id)"
            class="text-sm bg-red-600 text-white px-4 py-1 rounded-full hover:bg-red-700"
          >
            ❌ Remove
          </button>
        </li>
      </ul>

      <!-- Save Button -->
      <div class="text-center mt-6">
        <button
          @click="savePaper"
          :disabled="currentTotalMarks > examTotalMarks"
          :class="{
            'bg-blue-700 hover:bg-blue-800': currentTotalMarks <= examTotalMarks,
            'bg-gray-400 cursor-not-allowed': currentTotalMarks > examTotalMarks
          }"
          class="text-white px-6 py-2 rounded-full font-semibold"
        >
          💾 Save Paper
        </button>
        <!-- 📥 Download PDF Button -->
        <div class="text-center mt-4">
          <button
            @click="downloadPDF"
            class="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2 rounded-full font-semibold"
          >
            📥 Download Question Paper as PDF
          </button>
        </div>

        <p v-if="currentTotalMarks > examTotalMarks" class="text-red-600 font-semibold mt-2">
          ❌ You must reduce marks before saving.
        </p>
        <p v-if="successMessage" class="text-green-600 mt-4 font-medium">{{ successMessage }}</p>
      </div>
    </div>
  </div>
</template>





<script>
import axios from 'axios';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';


export default {
  data() {
    return {
      examId: this.$route.params.examId,
      questions: [],
      selectedQuestions: [],
      successMessage: '',
      paperTitle: '',
      totalMarks: 0,
      duration: 0,
      examTotalMarks: 0,
      examName: '',

    };
  },

  computed: {
    currentTotalMarks() {
      return this.selectedQuestions.reduce((sum, q) => sum + q.Marks, 0);
    },
    remainingMarks() {
      return this.examTotalMarks - this.currentTotalMarks;
    }
  },

  mounted() {
    this.fetchQuestions();
    this.fetchExamDetails();
  },
  methods: {
    async fetchQuestions() {
      try {
        const res = await axios.get(`http://localhost:5000/api/paper/questionbank/all/${this.examId}`);
        this.questions = res.data;
      } catch (err) {
        console.error("Failed to fetch questions:", err);
      }
    },
    async fetchExamDetails() {
      try {
        const res = await axios.get(`http://localhost:5000/api/paper/api/exam/details/${this.examId}`);
        console.log("📋 Exam Details:", res.data);
        this.examTotalMarks = res.data.total_marks; // Your backend should return this
        this.examName = res.data.exam_name;
      } catch (err) {
        console.error("❌ Failed to fetch exam details:", err);
        this.examTotalMarks = 0;
        this.examName = '';
      }
    },
    addQuestionToPaper(question) {
      const exists = this.selectedQuestions.find(q => q.Question_Id === question.Question_Id);
      if (exists) return;  
      
      const newTotal = this.currentTotalMarks + question.Marks;
      if (newTotal > this.examTotalMarks) {
        alert(`❌ Cannot add this question. Total marks would exceed ${this.examTotalMarks}.`);
        return;
      }
        this.selectedQuestions.push(question);
      },
    removeQuestion(id) {
    this.selectedQuestions = this.selectedQuestions.filter(q => q.Question_Id !== id);
    },
    savePaper() {
      const payload = {
        exam_id: this.$route.params.examId,
        questions: this.selectedQuestions.map(q => q.Question_Id)
      };
      
      fetch('http://localhost:5000/api/paper/save-question-paper', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      })
        .then(res => res.json())
        .then(data => {
          this.successMessage = '✅ Paper saved successfully!';
          setTimeout(() => {
            this.successMessage = '';
          }, 3000);
          console.log(data);
        })
        .catch(err => {
          console.error('❌ Error saving paper:', err);
          alert('❌ Failed to save the paper.');
        });
    },
    async randomizeQuestions() {
      try {
        const res = await fetch(`http://localhost:5000/api/paper/randomize/${this.examId}`, {
          method: 'POST'
      });
      const data = await res.json();
      this.selectedQuestions = data;
      alert('🎲 Random questions selected!');
    } catch (err) {
      console.error("❌ Failed to randomize:", err);
      alert("Failed to randomize questions");
    }
  },
  downloadPDF() {
    const doc = new jsPDF();
    const pageWidth = doc.internal.pageSize.getWidth();

    const title = `${this.examName} Question Paper`;

    // Center-align title
    doc.setFontSize(16);
    const textWidth = doc.getTextWidth(title);
    doc.text(title, (pageWidth - textWidth) / 2, 20);

    // Add metadata
    doc.setFontSize(12);
    doc.text(`Exam ID: ${this.examId}`, 14, 30);
    doc.text(`Total Marks: ${this.examTotalMarks}`, 14, 38);
    doc.text(`Total Questions: ${this.selectedQuestions.length}`, 14, 46);

    // Table
    const tableData = this.selectedQuestions.map((q, index) => [
      index + 1,
      q.Question_Text,
      q.Marks,
    ]);

    autoTable(doc, {
      head: [['Sr No.', 'Question', 'Marks']],
      body: tableData,
      startY: 55,
    });

    doc.save(`${this.examName.replace(/\s+/g, '_')}_Question_Paper.pdf`);
  }
  }
};
</script>

<style scoped>
input {
  border: 1px solid #ccc;
  padding: 6px;
  width: 100%;
  border-radius: 6px;
}
</style>
