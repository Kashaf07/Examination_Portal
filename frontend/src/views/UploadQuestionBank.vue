<template>
  <div class="max-w-md mx-auto mt-10 p-6 bg-white shadow-lg rounded-xl">
    <h2 class="text-2xl font-semibold text-gray-800 mb-6 text-center">
      Upload Question Bank (CSV)
    </h2>

    <p class="text-sm text-gray-600 text-center mb-2">
      Uploading for <strong>Exam ID: {{ examId }}</strong>
    </p>


    <!-- Download Sample as a Link -->
    <p class="text-sm text-gray-700 mb-4">
        Need a format?   
        <a
            href="http://localhost:5000/static/sample_question_bank.csv"
            download
            class="text-blue-600 underline hover:text-blue-800 transition duration-150"
        >
            Download Sample CSV Format
        </a>
    </p>


    <!-- File Input -->
    <div class="flex items-center border border-green-300 rounded-full overflow-hidden w-full max-w-md shadow-sm">
      <input
        type="file"
        @change="handleFileChange"
        accept=".csv"
        class="block w-full text-sm text-gray-500
               file:mr-4 file:py-2 file:px-4
               file:rounded file:border-0
               file:text-sm file:font-semibold
               file:bg-green-50 file:text-green-700
               hover:file:bg-green-100"
      />

      <button
      @click="uploadCSV"
      class="ml-auto bg-green-600 hover:bg-green-700 text-white font-medium text-sm px-6 py-2 h-full transition duration-200 rounded-full rounded-l-none"
      >
        Upload
      </button>
    </div>

  

     <!-- Optional Message -->
    <p v-if="message" class="mt-4 text-center text-green-700 fonr-bold">
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
      message: ''
    };
  },
  methods: {
    handleFileChange(event) {
      this.file = event.target.files[0];
    },
    async uploadCSV() {
      if (!this.file) {
        this.message = "Please select a CSV file.";
        return;
      }

      const formData = new FormData();
      formData.append('file', this.file);
      formData.append('exam_id', this.examId); // Form Id 

      try {
        const response = await fetch('http://localhost:5000/api/questions/upload-csv', {
          method: 'POST',
          body: formData
        });

        const result = await response.json();
        if (response.ok) {
          this.message = result.message;
        } else {
          this.message = `Error: ${result.error}`;
        }
      } catch (err) {
        this.message = 'An error occurred during upload.';
        console.error(err);
      }
    }
  },
  mounted() {
    this.examId = this.$route.params.examId; 
  }
};
</script>
