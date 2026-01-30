<template>
  <!-- Upload Card -->
  <div class="max-w-4xl mx-auto mt-8 bg-white rounded-2xl shadow-xl p-8">

    <!-- Download format -->
    <div class="text-center text-sm text-gray-700 mb-6">
      Need a format?
      <a
        href="http://localhost:5000/static/sample_question_bank.csv"
        download
        class="ml-1 text-blue-600 underline hover:text-blue-800 transition"
      >
        Download Sample CSV Template
      </a>
    </div>

    <!-- File Input Row -->
    <div
      class="flex items-center border border-green-300 rounded-full overflow-hidden shadow-sm"
    >
      <!-- Hidden input -->
      <input
        id="csv-file"
        type="file"
        accept=".csv"
        class="hidden"
        @change="handleFileChange"
      />

      <!-- Choose File -->
      <label
        for="csv-file"
        class="cursor-pointer px-6 py-3 bg-green-100 text-green-700 font-semibold text-sm"
      >
        Choose File
      </label>

      <!-- File name -->
      <span class="flex-1 px-4 text-sm text-gray-600 truncate">
        {{ fileName || 'No file chosen' }}
      </span>

      <!-- Upload button -->
      <button
        @click="uploadCSV"
        :disabled="!file"
        class="px-8 py-3 bg-green-500 text-white font-semibold text-sm
               hover:bg-green-600 transition
               disabled:bg-gray-300 disabled:cursor-not-allowed"
      >
        Upload CSV
      </button>
    </div>

    <!-- Success / Error message -->
    <p
      v-if="message"
      class="mt-5 text-center text-sm font-semibold text-green-600"
    >
      {{ message }}
    </p>

  </div>
</template>

<script>
export default {
  props: {
    examId: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      file: null,
      fileName: '',
      message: ''
    };
  },
  methods: {
    handleFileChange(e) {
      const f = e.target.files[0];
      this.file = f || null;
      this.fileName = f ? f.name : '';
      this.message = '';
    },
    clearMessageAfterDelay() {
      setTimeout(() => {
        this.message = '';
      }, 3000);
    },
    async uploadCSV() {
      if (!this.file) return;

      const formData = new FormData();
      formData.append('file', this.file);
      formData.append('exam_id', this.examId);
      formData.append('email', localStorage.getItem('faculty_email'));
      formData.append('role', 'Faculty');

      try {
        const res = await fetch(
          'http://localhost:5000/api/questions/upload-csv',
          { method: 'POST', body: formData }
        );
        const result = await res.json();

        this.message = res.ok
          ? (result.message || 'Questions uploaded successfully.')
          : (result.error || 'Upload failed.');

        if (res.ok) {
          this.file = null;
          this.fileName = '';
          document.getElementById('csv-file').value = '';
        }

        this.clearMessageAfterDelay();
      } catch (err) {
        console.error(err);
        this.message = 'An error occurred during upload.';
        this.clearMessageAfterDelay();
      }
    }
  }
};
</script>
