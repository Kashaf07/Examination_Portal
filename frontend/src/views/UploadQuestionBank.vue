<template>
  <div class="min-h-screen px-10 py-8 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
    <!-- Heading -->
    <div class="flex flex-col items-center gap-2 mb-10">
      <h2 class="text-4xl font-extrabold text-blue-800 flex items-center gap-3">
        <span class="text-5xl">📝</span>
        Add Question Bank
      </h2>
      <p class="text-lg text-gray-700">
        Adding questions for
        <span class="font-semibold text-purple-700">Exam ID: {{ examId }}</span>
      </p>
    </div>

    <!-- File row -->
    <div class="flex items-center justify-between max-w-4xl mx-auto mt-4">
      <!-- 1) REAL INPUT – HIDDEN -->
      <input
        id="csv-file"
        type="file"
        accept=".csv"
        class="hidden"
        @change="handleFileChange"
      />

      <!-- 2) ONLY THIS TEXT VISIBLE ON LEFT -->
      <label
        for="csv-file"
        class="cursor-pointer text-lg text-gray-900"
      >
        Choose File
        <span class="text-gray-600">
          {{ fileName || 'No file chosen' }}
        </span>
      </label>

      <!-- 3) GREEN BUTTON ON RIGHT -->
      <button
        @click="uploadCSV"
        class="flex items-center gap-2 bg-green-500 hover:bg-green-600
               text-white font-semibold text-lg px-10 py-3 rounded-full shadow-md
               transition duration-200"
      >
        <span class="text-2xl">📥</span>
        Upload CSV
      </button>
    </div>

    <p v-if="message" class="mt-8 text-center text-green-700 font-semibold">
      {{ message }}
    </p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      examId: this.$route.params.examId,
      file: null,
      fileName: '',
      message: ''
    };
  },
  methods: {
    handleFileChange(e) {
      const f = e.target.files[0];
      this.file = f;
      this.fileName = f ? f.name : '';
    },
    async uploadCSV() {
      if (!this.file) {
        this.message = 'Please select a CSV file.';
        return;
      }

      const formData = new FormData();
      formData.append('file', this.file);
      formData.append('exam_id', this.examId);
      formData.append('email', localStorage.getItem('faculty_email'));
      formData.append('role', 'Faculty');

      try {
        const res = await fetch('http://localhost:5000/api/questions/upload-csv', {
          method: 'POST',
          body: formData
        });
        const result = await res.json();
        this.message = res.ok
          ? (result.message || 'File uploaded successfully.')
          : (result.error || 'Unknown error occurred.');
      } catch (err) {
        console.error(err);
        this.message = 'An error occurred during upload.';
      }
    }
  }
};
</script>
