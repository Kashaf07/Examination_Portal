<template>
  <div class="min-h-screen p-10 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">

    <div class="text-center mb-6">
      <h2 class="text-4xl font-bold text-blue-800">
        🧑‍🎓 Add Students via Upload
      </h2>
    </div>

    <div class="max-w-3xl mx-auto bg-white p-10 rounded-2xl shadow-xl">

      <div class="mb-6 text-sm text-gray-700 text-center">
        Need a format?
        <a
          href="/sample/Applicants.csv"
          download
          class="text-blue-600 underline hover:text-blue-800"
        >
          Download Sample Excel Template
        </a>
      </div>

      <div class="flex items-center border border-green-300 rounded-full overflow-hidden shadow-sm w-full">
        <input
          type="file"
          @change="handleFileUpload"
          accept=".xlsx,.csv"
          class="block w-full text-sm text-gray-500
                 file:mr-4 file:py-2 file:px-4
                 file:rounded-full file:border-0
                 file:text-sm file:font-semibold
                 file:bg-green-100 file:text-green-700
                 hover:file:bg-green-200"
        />

        <button
          @click="uploadFile"
          :disabled="!selectedFile"
          class="ml-auto bg-green-600 text-white px-6 py-2 rounded-full rounded-l-none disabled:bg-gray-300"
        >
          Upload
        </button>
      </div>

      <p v-if="message" class="mt-6 text-center text-green-700 font-semibold">
        {{ message }}
      </p>

      <p v-if="error" class="mt-6 text-center text-red-600 font-semibold">
        {{ error }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import axios from "../utils/axiosInstance"

const selectedFile = ref(null)
const message = ref("")
const error = ref("")

const handleFileUpload = (e) => {
  selectedFile.value = e.target.files[0]
}

const uploadFile = async () => {
  if (!selectedFile.value) return

  const formData = new FormData()
  formData.append("file", selectedFile.value)

  try {
    const res = await axios.post("/upload_students", formData, {
      headers: { "Content-Type": "multipart/form-data" }
    })

    if (res.data.success) {
      message.value = `${res.data.message} (Inserted: ${res.data.inserted})`
      error.value = ""
      selectedFile.value = null
    } else {
      error.value = res.data.message || "Upload failed"
      message.value = ""
    }

  } catch (err) {
    error.value = err.response?.data?.message || "Server error during upload"
    message.value = ""
  }
}
</script>
