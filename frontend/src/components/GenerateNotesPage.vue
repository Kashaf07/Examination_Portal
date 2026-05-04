<template>
  <div class="min-h-screen p-8">
    <div class="max-w-7xl mx-auto">
      
      <!-- Header -->
      <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-800">Generate Notes with AI</h1>
            <p class="text-gray-600 mt-1">Create comprehensive study materials tailored to different learning levels</p>
          </div>
          <img src="/Gemini.png" alt="AI" class="w-16 h-16" />
        </div>
      </div>

      <!-- Configuration Bar -->
      <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
        <h2 class="text-lg font-bold text-gray-800 mb-4">Configure Notes</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-6 gap-4">
          <!-- Subject -->
          <div class="md:col-span-2">
            <label class="block text-sm font-semibold text-gray-700 mb-2">Subject *</label>
            <input
              v-model="formData.subject"
              placeholder="e.g., Python Programming"
              class="w-full border-2 border-gray-200 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-blue-400 transition-colors"
            />
          </div>

          <!-- Topics -->
          <div class="md:col-span-2">
            <label class="block text-sm font-semibold text-gray-700 mb-2">Topics *</label>
            <input
              v-model="formData.topics"
              placeholder="e.g., Variables, Data Types"
              class="w-full border-2 border-gray-200 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-blue-400 transition-colors"
            />
          </div>

          <!-- Difficulty -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Difficulty</label>
            <select
              v-model="formData.difficulty"
              class="w-full border-2 border-gray-200 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-blue-400 transition-colors"
            >
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
            </select>
          </div>

          <!-- Note Type -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Type</label>
            <select
              v-model="formData.note_type"
              class="w-full border-2 border-gray-200 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-blue-400 transition-colors"
            >
              <option value="Lecture Notes">Lecture</option>
              <option value="Revision Notes">Revision</option>
              <option value="Exam Preparation">Exam Prep</option>
              <option value="Concept Explanation">Concept</option>
              <option value="Assignment Guidelines">Assignment</option>
            </select>
          </div>
        </div>

        <!-- Length & Generate Button -->
        <div class="flex items-end gap-4 mt-4">
          <div class="flex-1">
            <label class="block text-sm font-semibold text-gray-700 mb-2">Length</label>
            <div class="flex gap-2">
              <button
                v-for="len in ['Short', 'Medium', 'Long']"
                :key="len"
                @click="formData.length = len"
                :class="[
                  'flex-1 py-2.5 px-4 rounded-lg font-semibold text-sm transition-all',
                  formData.length === len
                    ? 'bg-blue-600 text-white shadow-md'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                ]"
              >
                {{ len }}
              </button>
            </div>
          </div>

          <button
            @click="generateNotes"
            :disabled="loading || !isFormValid"
            class="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold px-8 py-2.5 rounded-lg shadow-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="!loading" class="flex items-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              Generate
            </span>
            <span v-else class="flex items-center gap-2">
              <svg class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Generating...
            </span>
          </button>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="mt-4 bg-red-50 border-2 border-red-200 rounded-lg p-3">
          <p class="text-red-600 text-sm font-semibold">{{ error }}</p>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="bg-white rounded-xl shadow-sm p-12 text-center">
        <div class="max-w-md mx-auto">
          <svg class="w-16 h-16 animate-spin text-blue-600 mx-auto mb-4" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <h3 class="text-xl font-bold text-gray-800 mb-2">Generating Your Notes...</h3>
          <p class="text-gray-600">AI is crafting comprehensive study materials</p>
        </div>
      </div>

      <!-- Generated Notes -->
      <div v-if="generatedNotes && !loading" class="bg-white rounded-xl shadow-sm overflow-hidden">
        
        <!-- Notes Header with Actions -->
        <div class="border-b border-gray-200 p-6">
          <div class="flex items-start justify-between mb-4">
            <div>
              <h2 class="text-2xl font-bold text-gray-800">{{ metadata.subject }}</h2>
              <p class="text-gray-600 mt-1">{{ metadata.topics }}</p>
            </div>
            <img src="/Gemini.png" alt="AI Generated" class="w-12 h-12" />
          </div>

          <div class="flex flex-wrap items-center gap-3">
            <!-- Metadata Tags -->
            <span class="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-xs font-semibold">
              {{ metadata.difficulty }} Level
            </span>
            <span class="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-xs font-semibold">
              {{ metadata.note_type }}
            </span>
            <span class="bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-semibold">
              {{ metadata.length }} Length
            </span>

            <div class="ml-auto flex gap-2">
              <!-- Copy Button -->
              <button
                @click="copyToClipboard"
                class="flex items-center gap-2 bg-gray-50 hover:bg-gray-100 text-gray-800 font-semibold px-5 py-2.5 rounded-lg border border-gray-300 transition-all shadow-sm"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
                <span class="text-black">{{ copied ? 'Copied!' : 'Copy' }}</span>
              </button>

              <!-- Download PDF -->
              <button
                @click="downloadAsPDF"
                :disabled="downloadingPDF"
                class="flex items-center gap-2 bg-red-50 hover:bg-red-100 text-red-700 font-semibold px-5 py-2.5 rounded-lg border border-red-200 transition-all shadow-sm disabled:opacity-50"
              >
                <img src="/pdf_icon.png" alt="PDF" class="w-5 h-5" />
                <span class="text-black">{{ downloadingPDF ? 'Generating...' : 'Download PDF' }}</span>
              </button>

              <!-- Download Word -->
              <button
                @click="downloadAsWord"
                class="flex items-center gap-2 bg-blue-50 hover:bg-blue-100 text-blue-700 font-semibold px-5 py-2.5 rounded-lg border border-blue-200 transition-all shadow-sm"
              >
                <img src="/word_icon.png" alt="Word" class="w-5 h-5" />
                <span class="text-black">Download Word</span>
              </button>

              <!-- Regenerate -->
              <button
                @click="regenerateNotes"
                class="flex items-center gap-2 bg-purple-600 hover:bg-purple-700 text-white font-semibold px-5 py-2.5 rounded-lg transition-all shadow-md"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Regenerate
              </button>
            </div>
          </div>
        </div>

        <!-- Notes Content -->
        <div class="p-8">
          <div 
            class="prose prose-lg max-w-none markdown-content"
            v-html="renderedMarkdown"
          ></div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!generatedNotes && !loading" class="bg-white rounded-xl shadow-sm p-12 text-center">
        <svg class="w-20 h-20 mx-auto text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h3 class="text-xl font-bold text-gray-800 mb-2">No Notes Generated Yet</h3>
        <p class="text-gray-600">Configure the settings above and click "Generate" to create AI-powered study materials</p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import axios from 'axios';
import { marked } from 'marked';
import { saveAs } from 'file-saver';
import { Document, Paragraph, TextRun, HeadingLevel, Packer } from 'docx';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

// Form data
const formData = ref({
  subject: '',
  topics: '',
  difficulty: 'Medium',
  note_type: 'Lecture Notes',
  length: 'Medium'
});

// State
const loading = ref(false);
const error = ref('');
const generatedNotes = ref('');
const metadata = ref({});
const copied = ref(false);
const downloadingPDF = ref(false);

// Computed
const isFormValid = computed(() => {
  return formData.value.subject.trim() && formData.value.topics.trim();
});

const renderedMarkdown = computed(() => {
  if (!generatedNotes.value) return '';
  return marked(generatedNotes.value);
});

// Methods
const generateNotes = async () => {
  loading.value = true;
  error.value = '';
  generatedNotes.value = '';
  
  try {
    const response = await axios.post(
      `http://${window.location.hostname}:5000/api/notes/generate`,
      {
        ...formData.value,
        email: localStorage.getItem('email'),
        role: localStorage.getItem('active_role')
      }
    );
    
    if (response.data.success) {
      generatedNotes.value = response.data.notes;
      metadata.value = response.data.metadata;
    } else {
      error.value = 'Failed to generate notes. Please try again.';
    }
  } catch (err) {
    console.error('Error generating notes:', err);
    error.value = err.response?.data?.error || 'An error occurred while generating notes.';
  } finally {
    loading.value = false;
  }
};

const regenerateNotes = () => {
  generateNotes();
};

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(generatedNotes.value);
    copied.value = true;
    setTimeout(() => {
      copied.value = false;
    }, 2000);
  } catch (err) {
    console.error('Failed to copy:', err);
  }
};

const downloadAsPDF = async () => {
  downloadingPDF.value = true;
  try {
    const pdf = new jsPDF('p', 'mm', 'a4');
    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();
    const margin = 15;
    const contentWidth = pageWidth - (margin * 2);
    let yPosition = margin;

    // Add metadata header
    pdf.setFontSize(20);
    pdf.setFont('helvetica', 'bold');
    pdf.text(metadata.value.subject, margin, yPosition);
    yPosition += 10;

    pdf.setFontSize(10);
    pdf.setFont('helvetica', 'normal');
    pdf.text(`Topics: ${metadata.value.topics}`, margin, yPosition);
    yPosition += 6;
    pdf.text(`Difficulty: ${metadata.value.difficulty} | Type: ${metadata.value.note_type}`, margin, yPosition);
    yPosition += 10;

    // Parse and add content
    const lines = generatedNotes.value.split('\n');
    pdf.setFontSize(11);
    
    for (const line of lines) {
      if (yPosition > pageHeight - margin) {
        pdf.addPage();
        yPosition = margin;
      }

      if (line.startsWith('## ')) {
        pdf.setFontSize(16);
        pdf.setFont('helvetica', 'bold');
        const text = line.replace('## ', '');
        pdf.text(text, margin, yPosition);
        yPosition += 8;
        pdf.setFontSize(11);
        pdf.setFont('helvetica', 'normal');
      } else if (line.startsWith('### ')) {
        pdf.setFontSize(14);
        pdf.setFont('helvetica', 'bold');
        const text = line.replace('### ', '');
        pdf.text(text, margin, yPosition);
        yPosition += 7;
        pdf.setFontSize(11);
        pdf.setFont('helvetica', 'normal');
      } else if (line.trim()) {
        const cleanLine = line.replace(/[*_`#]/g, '');
        const splitText = pdf.splitTextToSize(cleanLine, contentWidth);
        pdf.text(splitText, margin, yPosition);
        yPosition += splitText.length * 6;
      } else {
        yPosition += 4;
      }
    }

    pdf.save(`${formData.value.subject.replace(/\s+/g, '_')}_Notes.pdf`);
  } catch (err) {
    console.error('Error generating PDF:', err);
    alert('Failed to generate PDF');
  } finally {
    downloadingPDF.value = false;
  }
};

const downloadAsWord = async () => {
  try {
    const lines = generatedNotes.value.split('\n');
    const children = [];
    
    // Add metadata header
    children.push(
      new Paragraph({
        text: metadata.value.subject,
        heading: HeadingLevel.HEADING_1,
      }),
      new Paragraph({
        text: `Topics: ${metadata.value.topics}`,
      }),
      new Paragraph({
        text: `Difficulty: ${metadata.value.difficulty} | Type: ${metadata.value.note_type}`,
      }),
      new Paragraph({ text: '' })
    );
    
    // Parse content
    lines.forEach(line => {
      if (line.startsWith('## ')) {
        children.push(new Paragraph({
          text: line.replace('## ', ''),
          heading: HeadingLevel.HEADING_2,
        }));
      } else if (line.startsWith('### ')) {
        children.push(new Paragraph({
          text: line.replace('### ', ''),
          heading: HeadingLevel.HEADING_3,
        }));
      } else if (line.trim()) {
        children.push(new Paragraph({
          children: [new TextRun(line.replace(/[*_`]/g, ''))],
        }));
      } else {
        children.push(new Paragraph({ text: '' }));
      }
    });
    
    const doc = new Document({
      sections: [{
        properties: {},
        children: children,
      }],
    });
    
    const blob = await Packer.toBlob(doc);
    saveAs(blob, `${formData.value.subject.replace(/\s+/g, '_')}_Notes.docx`);
  } catch (err) {
    console.error('Error generating Word document:', err);
    alert('Failed to generate Word document');
  }
};
</script>

<style scoped>
/* Markdown content styling */
:deep(.markdown-content) {
  color: #1f2937;
}

:deep(.markdown-content h1) {
  font-size: 1.875rem;
  font-weight: 700;
  color: #111827;
  margin-top: 2rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #bfdbfe;
}

:deep(.markdown-content h2) {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}

:deep(.markdown-content h3) {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-top: 1rem;
  margin-bottom: 0.5rem;
}

:deep(.markdown-content p) {
  margin-bottom: 1rem;
  line-height: 1.75;
}

:deep(.markdown-content ul),
:deep(.markdown-content ol) {
  margin-bottom: 1rem;
  padding-left: 2rem;
}

:deep(.markdown-content li) {
  margin-top: 0.5rem;
}

:deep(.markdown-content code) {
  background: #ffffff;
  border: 2px solid #000000;
  color: #000000;
  padding: 0.25rem 0.5rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-weight: 500;
}

:deep(.markdown-content pre) {
  background: #ffffff;
  border: 2px solid #000000;
  color: #000000;
  padding: 1.5rem;
  border-radius: 0.5rem;
  overflow-x: auto;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  line-height: 1.6;
}

:deep(.markdown-content pre code) {
  background: transparent;
  border: none;
  color: #000000;
  padding: 0;
  font-weight: normal;
}

:deep(.markdown-content blockquote) {
  border-left: 4px solid #3b82f6;
  padding-left: 1rem;
  font-style: italic;
  color: #374151;
  margin: 1rem 0;
  background-color: #eff6ff;
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
  border-radius: 0 0.5rem 0.5rem 0;
}

:deep(.markdown-content strong) {
  font-weight: 700;
  color: #111827;
}

:deep(.markdown-content a) {
  color: #2563eb;
  text-decoration: underline;
}

:deep(.markdown-content table) {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
}

:deep(.markdown-content th),
:deep(.markdown-content td) {
  border: 1px solid #d1d5db;
  padding: 0.5rem 1rem;
  text-align: left;
}

:deep(.markdown-content th) {
  background-color: #f3f4f6;
  font-weight: 600;
}
</style>
