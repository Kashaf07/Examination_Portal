<template>
  <div class="min-h-screen p-10 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
    
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

    <!-- Heading -->
    <div class="text-center mb-6">
      <h1 class="text-4xl font-bold text-blue-800 flex justify-center items-center gap-2">
        📚 Make Question Paper for {{ examName }}
      </h1>
      <p class="text-gray-700">
        Select questions for <strong class="text-purple-700">Exam ID: {{ examId }}</strong>
      </p><br>
      <div class="flex flex-wrap justify-center gap-3">

        <button @click="randomizeQuestions"
        class="action-btn randomize-btn text-sm">
          🎲 Randomize Questions
        </button>
        <button @click="savePaper"
        class="action-btn text-sm" 
        :disabled="!isPaperComplete"
        :class="!isPaperComplete ? 'opacity-60 cursor-not-allowed' : ''"
        title="Save is enabled only when selected marks equal allowed total">
          💾 Save Paper
        </button>
        <button @click="downloadPDF"
        class="action-btn text-sm">
          📥 Download Question Paper as PDF
        </button>
        
      </div>
    </div>

    <p v-if="currentTotalMarks > examTotalMarks" class="text-red-600 font-semibold mt-2 mb-2 text-center">
      ❌ You must reduce marks before saving.
    </p>
    <p v-if="successMessage" class="text-green-600 mt-4 mb-4 font-medium text-center">{{ successMessage }} </p>
      

    <!-- Marks Summary -->
    <div class="bg-yellow-100 border-l-4 border-yellow-500 rounded-lg p-4 mb-8 shadow-md max-w-2xl mx-auto">
      <p class="text-lg font-semibold text-red-700">📋 Total Allowed Marks: <span class="text-blue-700">{{ examTotalMarks }}</span></p>
      <p class="text-green-700">✅ Current Total Marks: {{ currentTotalMarks }}</p>
      <p class="text-gray-800">🟢 Remaining Marks: {{ remainingMarks }}</p>
    </div>


    
    <!-- Question Cards -->
    <div v-if="unselectedQuestions.length" class="mt-12 space-y-4 max-w-3xl mx-auto">
      <h2 class="text-xl font-semibold mb-4 text-purple-700">📚 Available Questions</h2>
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
      examDate: '',
      examTime: '',
    };
  },

  computed: {
    currentTotalMarks() {
      return this.selectedQuestions.reduce((sum, q) => sum + q.Marks, 0);
    },
    remainingMarks() {
      return this.examTotalMarks - this.currentTotalMarks;
    },
    unselectedQuestions() {
      return this.questions.filter(q =>
        !this.selectedQuestions.some(sq => sq.Question_Id === q.Question_Id)
      );
    },
    isPaperComplete() {
    return this.currentTotalMarks === this.examTotalMarks && this.selectedQuestions.length > 0;
    }
  },

  mounted() {
    this.fetchQuestions();
    this.fetchExamDetails();
    this.fetchSelectedQuestions();
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
    async fetchQuestions() {
      try {
        const res = await axios.get(`http://localhost:5000/api/paper/questionbank/all/${this.examId}`);
        this.questions = res.data;
      } catch (err) {
        console.error("Failed to fetch questions:", err);
      }
    },
    async fetchPaperQuestionsForPDF() {
      try {
        const res = await axios.get(
          `http://localhost:5000/api/questions/paper/${this.examId}`
        )
        return res.data
      } catch (err) {
        console.error("❌ Failed to fetch paper questions:", err)
        return []
      }
    },
    async fetchSelectedQuestions() {
      try {
        const res = await axios.get(`http://localhost:5000/api/paper/selected/${this.examId}`);
        this.selectedQuestions = res.data;
      } catch (err) {
        console.error("❌ Failed to fetch selected questions:", err);
      }
    },
    async fetchExamDetails() {
      try {
        const res = await axios.get(`http://localhost:5000/api/paper/api/exam/details/${this.examId}`);
        console.log("📋 Exam Details:", res.data);
        this.examTotalMarks = res.data.total_marks; // Your backend should return this
        this.examName = res.data.exam_name;
        this.examDate = res.data.exam_date || res.data.Exam_Date
        this.examTime = res.data.exam_time || res.data.Exam_Time
      } catch (err) {
        console.error("❌ Failed to fetch exam details:", err);
        this.examTotalMarks = 0;
        this.examName = '';
      }
    },
    formatTime12h(time) {
      if (!time) return ''
      const [h, m] = time.split(':')
      const hour = Number(h)
      const suffix = hour >= 12 ? 'PM' : 'AM'
      const formattedHour = hour % 12 || 12
      return `${formattedHour}:${m} ${suffix}`
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
      // client-side guard: only allow save if exact equality
      if (!this.isPaperComplete) {
        // Provide a helpful message
        if (this.currentTotalMarks > this.examTotalMarks) {
          alert(`❌ Total marks exceed the allowed ${this.examTotalMarks}. Please remove or reduce questions.`);
        } else {
          alert(`❌ Total marks must be exactly ${this.examTotalMarks} to save the paper. Current total: ${this.currentTotalMarks}.`);
        }
        return;
      }
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
  async downloadPDF() {
    const questions = await this.fetchPaperQuestionsForPDF()
    if (!questions.length) {
      alert("No questions found for paper")
      return
    }

    const doc = new jsPDF("p", "mm", "a4")
    let y = 20

    /* ================= HEADER ================= */
    doc.setFontSize(16)
    doc.setFont("helvetica", "bold")
    doc.text(this.examName.toUpperCase(), 105, y, { align: "center" })

    y += 8
    doc.setFontSize(11)
    doc.setFont("helvetica", "normal")
    doc.text(`Exam ID: ${this.examId}`, 14, y)
    doc.text(`Date: ${this.examDate}`, 150, y)    

    y += 6
    doc.text(`Total Marks: ${this.examTotalMarks}`, 14, y)
    doc.text(`Time: ${this.formatTime12h(this.examTime)}`,150,y)
    y += 6
    doc.line(14, y, 196, y)
    y += 8

    /* ================= QUESTIONS ================= */
    questions.forEach((q, index) => {
      if (y > 270) {
        doc.addPage()
        y = 20
      }

      // Question text (left)
      doc.setFont("helvetica", "bold")
      doc.text(`${index + 1}. ${q.Question_Text}`, 14, y)

      // Marks aligned with question (right)
      doc.setFontSize(9)
      doc.text(`[${q.Marks} Marks]`, 196, y, { align: "right" })
      doc.setFontSize(11)

      // Move down AFTER question row
      y += 6
      doc.setFont("helvetica", "normal")

      /* ===== MCQ ===== */
      if (q.Question_Type === "MCQ") {
        if (q.Option_A) doc.text(`A. ${q.Option_A}`, 18, y), (y += 5)
        if (q.Option_B) doc.text(`B. ${q.Option_B}`, 18, y), (y += 5)
        if (q.Option_C) doc.text(`C. ${q.Option_C}`, 18, y), (y += 5)
        if (q.Option_D) doc.text(`D. ${q.Option_D}`, 18, y), (y += 5)
      }

      /* ===== TRUE / FALSE ===== */
      else if (q.Question_Type === "TF") {
        doc.text("A. True", 18, y)
        y += 5
        doc.text("B. False", 18, y)
        y += 5
      }

      /* ===== FILL / ONE WORD ===== */
      else {
        doc.text("______________________________", 18, y)
        y += 6
      }

      y += 6
    })

    /* ================= FOOTER ================= */
    doc.setFontSize(9)
    doc.text("— End of Question Paper —", 105, 290, { align: "center" })

    doc.save(`${this.examName.replace(/\s+/g, "_")}_Question_Paper.pdf`)
  }
  }
};
</script>

<style scoped>

.action-btn {
  background: linear-gradient(to right, #3271d5, #1e52c3); /* blue gradient */
  padding: 0.5rem 1.25rem;
  border-radius: 9999px; /* rounded-full */
  font-weight: 600;
  color: white;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
}

.action-btn:hover {
  background: linear-gradient(to right, #2a489b, #15349c); /* darker on hover */
  transform: scale(1.03);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
}

.randomize-btn {
  background: linear-gradient(to right, #9449da, #6b1ab1); /* purple */
}
.randomize-btn:hover {
  background: linear-gradient(to right, #6b21a8, #581c87);
}

input {
  border: 1px solid #ccc;
  padding: 6px;
  width: 100%;
  border-radius: 6px;
}
</style>