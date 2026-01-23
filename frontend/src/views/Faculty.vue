<template>
  <div class="container-wrapper">
    <div class="min-h-screen flex" style="background: linear-gradient(to bottom right, #E3F2FD, #F3E5F5, #FCE4EC);">

    <!-- Sidebar -->
    <aside
      :class="[
        'fixed left-0 top-0 h-screen border-r border-gray-200 text-gray-800 transition-all duration-300 z-50 shadow-lg',
        sidebarOpen ? 'w-64' : 'w-20'
      ]"
      style="background: linear-gradient(180deg, #B6D4F2, #DCEBFA);"
    >

      <!-- Sidebar Header -->
      <div class="px-4 py-3 border-b border-white/40">
        <div class="flex items-center justify-between">

          <!-- When Closed: Show Avatar and Hamburger -->
          <template v-if="!sidebarOpen">
            <button
              @click="sidebarOpen = !sidebarOpen"
              class="w-10 h-10 flex items-center justify-center rounded-xl
                     bg-gradient-to-br from-blue-500 to-indigo-600
                     text-white shadow-md hover:shadow-lg transition"
              title="Open Menu"
            >
              <svg
                class="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                stroke-width="2"
                stroke-linecap="round"
              >
                <line x1="4" y1="6" x2="20" y2="6" />
                <line x1="4" y1="12" x2="20" y2="12" />
                <line x1="4" y1="18" x2="20" y2="18" />
              </svg>
            </button>
          </template>

          <!-- When Open: Show Avatar + Name and Hamburger -->
          <template v-else>
            <div class="flex items-center gap-3 overflow-hidden">
              <div class="w-9 h-9 bg-gradient-to-br from-blue-500 to-indigo-600 text-white flex items-center justify-center rounded-full font-bold shrink-0 shadow-md">
                {{ facultyInitial }}
              </div>

              <div class="leading-tight truncate">
                <p class="font-semibold text-gray-800 text-sm truncate">
                  {{ facultyName }}
                </p>
                <p class="text-xs text-gray-600">
                  Faculty Member
                </p>
              </div>
            </div>

            <button
              @click="sidebarOpen = !sidebarOpen"
              class="w-9 h-9 flex items-center justify-center rounded-lg border-0 text-white hover:bg-blue-700 transition bg-blue-600 shrink-0"
            >
              <svg
                class="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                stroke-width="2"
              >
                <line x1="4" y1="6" x2="20" y2="6" stroke-linecap="round"/>
                <line x1="4" y1="12" x2="20" y2="12" stroke-linecap="round"/>
                <line x1="4" y1="18" x2="20" y2="18" stroke-linecap="round"/>
              </svg>
            </button>
          </template>

        </div>
      </div>

      <!-- Navigation Menu -->
      <nav class="flex-1 py-4 px-3 space-y-1.5 overflow-y-auto" style="max-height: calc(100vh - 200px);">
        <button
          v-for="tab in visibleTabs"
          :key="tab.id"
          @click="goToTab(tab.id)"
          :class="[
            'w-full flex items-center gap-3 px-4 py-2.5 rounded-xl transition-all duration-200 group relative',
            activeTab === tab.id 
              ? 'bg-blue-100 text-blue-700 shadow-sm' 
              : 'hover:bg-white hover:bg-opacity-40 text-gray-700 hover:text-gray-900'
          ]"
        >
          <!-- Icon Image -->
          <div class="icon-container">
            <img 
              :src="'/' + tab.icon + '.png'" 
              :alt="tab.name"
              class="icon-image"
            />
          </div>

          <!-- Label -->
          <span 
            v-if="sidebarOpen" 
            class="font-semibold text-sm"
          >
            {{ tab.name }}
          </span>

          <!-- Tooltip for collapsed state -->
          <div
            v-if="!sidebarOpen"
            class="absolute left-full ml-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all whitespace-nowrap z-50"
          >
            {{ tab.name }}
          </div>
        </button>
      </nav>

      <!-- Bottom Actions -->
      <div class="absolute bottom-0 left-0 right-0 p-3 border-t border-white border-opacity-30 space-y-2">
        <!-- Switch Role Button -->
        <div class="relative">
          <button
            v-if="canSwitch"
            @click="toggleRoleMenu"
            :class="[
              'w-full flex items-center gap-3 px-4 py-2.5 rounded-xl transition-all duration-200 group',
              'bg-green-500 hover:bg-green-600 text-white shadow-md hover:shadow-lg'
            ]"
          >
            <div class="icon-container">
              <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
              </svg>
            </div>
            <span v-if="sidebarOpen" class="font-semibold text-sm">Switch Role</span>

            <!-- Tooltip for collapsed state -->
            <div
              v-if="!sidebarOpen"
              class="absolute left-full ml-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all whitespace-nowrap z-50"
            >
              Switch Role
            </div>
          </button>

          <!-- Role Dropdown Menu -->
          <div
            v-if="showRoleMenu"
            class="absolute bottom-0 left-full ml-2 bg-white rounded-xl shadow-2xl border border-gray-200 py-3 z-[60] min-w-[280px]"
          >
            <div class="px-5 py-3 text-base text-gray-600 border-b border-gray-100">
              Available Roles
            </div>

            <button
              @click.stop="selectRole('admin')"
              class="w-full px-5 py-4 text-left text-base hover:bg-blue-50 transition-colors text-gray-700 font-semibold hover:text-blue-600"
            >
              <div class="flex items-center justify-between">
                <span>Administrator</span>
              </div>
            </button>
          </div>
        </div>

        <!-- Logout Button -->
        <button
          @click="logout"
          :class="[
            'w-full flex items-center gap-3 px-4 py-2.5 rounded-xl transition-all duration-200 group',
            'bg-red-500 hover:bg-red-600 text-white shadow-md hover:shadow-lg relative'
          ]"
        >
          <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          <span v-if="sidebarOpen" class="font-semibold text-sm">Logout</span>

          <!-- Tooltip for collapsed state -->
          <div
            v-if="!sidebarOpen"
            class="absolute left-full ml-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all whitespace-nowrap z-50"
          >
            Logout
          </div>
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main 
      :class="[
        'flex-1 transition-all duration-300',
        sidebarOpen ? 'ml-64' : 'ml-20'
      ]"
    >
      <!-- Main Content Area -->
      <div class="p-8 pt-8 max-w-full overflow-x-hidden"> 

        <!-- Welcome Screen (shown when activeTab is null) -->
        <div
          v-if="activeTab === null"
          class="flex items-center justify-center min-h-[80vh]"
        >
          <div class="text-center">
            <div class="mb-6">
              <div class="w-24 h-24 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center mx-auto shadow-2xl">
                <span class="text-4xl text-white font-bold">{{ facultyInitial }}</span>
              </div>
            </div>
            <h1 class="text-4xl font-bold text-gray-800 mb-4">
              Welcome, {{ facultyName }}!
            </h1>
            <p class="text-lg text-gray-600 mb-8">
              Select a menu item from the sidebar to get started
            </p>
          </div>
        </div>

        <!-- Content Area (shown when specific tab is selected) -->
        <div v-else>
          <!-- My Exams View -->
          <div v-if="activeTab === 'my-exams'">
            <div class="mb-8">
              <h1 class="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
                My Exams
              </h1>
              <p class="text-gray-600 mt-2">Create and manage your exams</p>
            </div>

    <!-- Button Group -->
    <div class="flex gap-4 mb-6">
      <button
        @click="toggleExamForm"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        {{ showForm ? 'Close' : 'Create Exam' }}
      </button>
      <button 
        @click="toggleGroups"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        {{ showGroups ? 'Close' : 'Groups' }}
      </button>
      <button 
        @click="toggleApplicantForm"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        {{ showApplicantForm ? 'Close' : 'Add Applicants' }}
      </button>
      <button
        @click="navigateTo('UploadStudents')"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Upload Applicants
      </button>
    </div>

    <!-- Create Exam Form -->
    <div
      v-if="showForm"
      class="max-w-3xl mx-auto mb-8 bg-white/80 backdrop-blur-lg shadow-xl border border-white/40 rounded-2xl p-8 transition-all"
    >
      <h2 class="text-2xl font-bold mb-6 text-gray-800 flex items-center gap-2">
        Create New Exam
      </h2>

      <form @submit.prevent="submitExam" class="space-y-6">

        <!-- GRID -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">

          <!-- Exam Name -->
          <div class="flex flex-col gap-1">
            <label class="font-semibold text-gray-700">Exam Name</label>
            <div class="relative">
              <input
                v-model="exam.exam_name"
                type="text"
                placeholder="Enter exam name"
                required
                class="w-full border border-gray-300 px-4 py-2.5 rounded-xl focus:ring-2 focus:ring-blue-400 focus:border-blue-500 outline-none transition"
              />
            </div>
          </div>

          <!-- Exam Date -->
          <div class="flex flex-col gap-1">
            <label class="font-semibold text-gray-700">Exam Date</label>
            <input
              v-model="exam.exam_date"
              type="date"
              required
              :min="todayDate"
              class="w-full border border-gray-300 px-4 py-2.5 rounded-xl focus:ring-2 focus:ring-blue-400 focus:border-blue-500 outline-none transition"
            />
          </div>

          <!-- Exam Time -->
          <div class="flex flex-col gap-1">
            <label class="font-semibold text-gray-700">Exam Time</label>
            <input
              v-model="exam.exam_time"
              type="time"
              required
              class="w-full border border-gray-300 px-4 py-2.5 rounded-xl focus:ring-2 focus:ring-blue-400 focus:border-blue-500 outline-none transition"
            />
          </div>

          <!-- Duration -->
          <div class="flex flex-col gap-1">
            <label class="font-semibold text-gray-700">Duration (Minutes)</label>
            <input
              v-model="exam.duration"
              type="number"
              min="1"
              placeholder="e.g., 60"
              required
              class="w-full border border-gray-300 px-4 py-2.5 rounded-xl focus:ring-2 focus:ring-blue-400 focus:border-blue-500 outline-none transition"
            />
          </div>

          <!-- Total Questions -->
          <div class="flex flex-col gap-1">
            <label class="font-semibold text-gray-700">Total Questions</label>
            <input
              v-model="exam.total_questions"
              type="number"
              min="1"
              required
              placeholder="e.g., 50"
              class="w-full border border-gray-300 px-4 py-2.5 rounded-xl focus:ring-2 focus:ring-blue-400 focus:border-blue-500 outline-none transition"
            />
          </div>

          <!-- Max Marks -->
          <div class="flex flex-col gap-1">
            <label class="font-semibold text-gray-700">Max Marks</label>
            <input
              v-model="exam.max_marks"
              type="number"
              min="1"
              required
              placeholder="e.g., 100"
              class="w-full border border-gray-300 px-4 py-2.5 rounded-xl focus:ring-2 focus:ring-blue-400 focus:border-blue-500 outline-none transition"
            />
          </div>

        </div>

        <!-- Error Message -->
        <p
          v-if="examSubmitMessage"
          class="text-red-600 font-medium text-sm mt-1"
        >
          {{ examSubmitMessage }}
        </p>

        <!-- Footer Buttons -->
        <div class="flex justify-end gap-4 pt-4">

          <button
            @click="toggleExamForm"
            type="button"
            class="bg-gray-300 text-gray-700 px-6 py-2 rounded-xl hover:bg-gray-400 transition font-semibold shadow-md hover:shadow-lg"
          >
            Cancel
          </button>

          <button
            type="submit"
            class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition font-semibold shadow-md hover:shadow-lg"
          >
            Create Exam
          </button>

        </div>

      </form>
    </div>


    <!-- Groups Panel -->
    <div
      v-if="showGroups"
      class="max-w-8xl mx-auto rounded-xl shadow-xl p">
      <FacultyGroups @closeGroup="showGroups = false" />
    </div>


    <!-- Add Applicants Panel -->
    <div v-if="showApplicantForm" 
     class="max-w-5xl mx-auto bg-white rounded-xl shadow-xl p-7">
      <AddApplicantsPage @closeAddApplicant="showApplicantForm = false" />     
    </div>

    
  <!-- Exam Tables Only Visible When on Dashboard -->
  <div v-if="currentTab === 'Dashboard'">
    <!-- Exam Table (Upcoming/Created) -->
    <div v-if="createdExams.length" class="mt-8">
      <h2 class="text-2xl font-semibold mb-4">Created Exams</h2>
      <table class="min-w-full border text-sm text-left">
        <thead class="bg-gray-200">
          <tr>
            <th class="px-4 py-2">Exam Name</th>
            <th class="px-4 py-2">Date</th>
            <th class="px-4 py-2">Time</th>
            <th class="px-4 py-2">Duration (Min)</th>
            <th class="px-4 py-2">Total Questions</th>
            <th class="px-4 py-2">Max Marks</th>
            <th class="px-4 py-2 text-center">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="exam in createdExams" :key="exam.Exam_Id" class="border-t">
            <td class="px-4 py-2">{{ exam.Exam_Name }}</td>
            <td class="px-4 py-2">{{ exam.Exam_Date }}</td>
            <td class="px-4 py-2">{{ exam.Exam_Time }}</td>
            <td class="px-4 py-2">{{ exam.Duration_Minutes }}</td>
            <td class="px-4 py-2">{{ exam.Total_Questions }}</td>
            <td class="px-4 py-2">{{ exam.Max_Marks }}</td>
            <td class="px-4 py-3">
  <div class="flex flex-wrap justify-center items-center gap-2">

    <!-- Add Students -->
    <button
      @click="navigateTo('AddApplicants_exam', exam.Exam_Id)"
      class="flex items-center gap-1 bg-blue-500 text-white px-3 py-1.5 rounded-full text-xs shadow hover:scale-105 transition"
    >
      Add Students
    </button>

                          <button
                            @click="navigateTo('AddQuestion', exam.Exam_Id)"
                            class="bg-green-500 text-white px-3 py-1.5 rounded-full text-xs shadow hover:scale-105 transition font-semibold"
                          >
                            Question Bank
                          </button>

                          <span
                            v-if="examStatus[exam.Exam_Id]?.has_question_bank"
                            class="text-green-600 text-lg"
                            title="Completed"
                          >
                            ✔
                          </span>
                          <span
                            v-else
                            class="text-yellow-600 text-lg"
                            title="Pending"
                          >
                            ⏳
                          </span>

                          <button
                            @click="navigateTo('MakeQuestionPaper', exam.Exam_Id)"
                            class="bg-purple-500 text-white px-3 py-1.5 rounded-full text-xs shadow hover:scale-105 transition font-semibold"
                          >
                            Question Paper
                          </button>

                          <span
                            v-if="examStatus[exam.Exam_Id]?.has_question_paper"
                            class="text-green-600 text-lg"
                            title="Completed"
                          >
                            ✔
                          </span>
                          <span
                            v-else
                            class="text-yellow-600 text-lg"
                            title="Pending"
                          >
                            ⏳
                          </span>

                          <button
                            @click="deleteExam(exam.Exam_Id)"
                            class="bg-red-500 text-white px-3 py-1.5 rounded-full text-xs shadow hover:scale-105 transition font-semibold"
                          >
                            🗑 Delete
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div v-else class="mt-8 text-gray-500 text-center text-lg py-12 bg-white rounded-xl shadow">
              No exams created yet.
            </div>

            <!-- Conducted Exams Table -->
            <div v-if="conductedExams && conductedExams.length" class="mt-12">
              <h2 class="text-2xl font-semibold mb-4 text-gray-800">Conducted Exams</h2>
              <div class="bg-white rounded-xl shadow-lg overflow-hidden">
                <table class="min-w-full">
                  <thead class="bg-gradient-to-r from-blue-50 to-indigo-50">
                    <tr>
                      <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Exam Name</th>
                      <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Date</th>
                      <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Total Applicants</th>
                      <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Attempted</th>
                      <th class="px-6 py-4 text-center text-sm font-bold text-gray-700">Actions</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-gray-200">
                    <tr v-for="exam in conductedExams" :key="exam.Exam_Id" class="hover:bg-gray-50 transition">
                      <td class="px-6 py-4 text-sm text-gray-800 font-medium">{{ exam.Exam_Name || 'N/A' }}</td>
                      <td class="px-6 py-4 text-sm text-gray-600">{{ formatDate(exam.Exam_Date) }}</td>
                      <td class="px-6 py-4 text-sm text-gray-600">{{ exam.total_applicants || 0 }}</td>
                      <td class="px-6 py-4 text-sm text-gray-600">{{ exam.attempted_applicants || 0 }}</td>
                      <td class="px-6 py-4 text-center">
                        <button
                          @click="navigateTo('ViewResponses', exam.Exam_Id)"
                          class="bg-purple-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-purple-700 shadow-md hover:shadow-lg transition font-semibold"
                        >
                          View Responses
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- Groups View -->
          <div v-else-if="activeTab === 'groups'" class="w-full min-h-[85vh]">
  <Groups />
</div>


          <!-- Add Applicants View -->
          <div v-else-if="activeTab === 'add-applicants'" class="w-full min-h-[85vh]">
  <AddApplicantsPage />
</div>


          <!-- Upload Students View -->
          <div v-else-if="activeTab === 'upload-students'" class="w-full min-h-[85vh]">
  <UploadStudents />
</div>


        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from '../utils/axiosInstance'
import FacultyGroups from "../views/Groups.vue"
import AddApplicantsPage from "../views/AddApplicantsPage.vue"
import AddApplicantsPage from './AddApplicantsPage.vue'
import UploadStudents from './UploadStudents.vue'
import Groups from './Groups.vue'



const router = useRouter()
const currentTab = ref("Dashboard")  // default section
const showGroups = ref(false)


// Roles and Auth
const roles = JSON.parse(localStorage.getItem("roles") || "[]")
const activeRole = ref(localStorage.getItem("active_role"))
const canSwitch = roles.includes("Admin") && roles.includes("Faculty")

// Faculty Info
const facultyName = ref(localStorage.getItem("name") || "Faculty")
const email = localStorage.getItem("email")
const facultyEmail = email
const facultyInitial = computed(() => facultyName.value.charAt(0).toUpperCase())

// Sidebar state
const sidebarOpen = ref(true)
const showRoleMenu = ref(false)
const activeTab = ref(null)

// All available tabs
const allTabs = [
  { id: "my-exams", name: "My Exams", icon: "exams", access: "create_exam" },
  { id: "groups", name: "Groups", icon: "groups", access: "view_groups" },
  { id: "add-applicants", name: "Add Applicants", icon: "applicants", access: "add_applicants" },
  { id: "upload-students", name: "Upload Students", icon: "applicants", access: "upload_students" }
]

// Faculty permissions (this should come from API in real implementation)
const facultyPermissions = ref({
  create_exam: true,
  view_groups: true,
  add_applicants: true,
  upload_students: true
})

// Filtered tabs based on permissions
const visibleTabs = computed(() => {
  return allTabs.filter(tab => facultyPermissions.value[tab.access])
})

// Exam data
const showForm = ref(false)
const examSubmitMessage = ref('')
const createdExams = ref([])
const conductedExams = ref([])
const examStatus = ref({})

const todayDate = computed(() => {
  const today = new Date()
  const year = today.getFullYear()
  const month = String(today.getMonth() + 1).padStart(2, '0')
  const day = String(today.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
})

const exam = ref({
  exam_name: '',
  exam_date: '',
  exam_time: '',
  duration: '',
  total_questions: '',
  max_marks: '',
  faculty_email: facultyEmail
})

// Auth check on mount
onMounted(() => {
  if (activeRole.value !== "Faculty") {
    router.push("/")
  } else {
    fetchExamsAndCategorize()
    activeTab.value = 'my-exams'

  }

  // Close role menu when clicking outside
  const handleClickOutside = (e) => {
    if (showRoleMenu.value && !e.target.closest('.relative')) {
      showRoleMenu.value = false
    }
  }
  
  document.addEventListener('click', handleClickOutside)
})

const toggleExamForm = () => {
  showForm.value = !showForm.value
  examSubmitMessage.value = ''
}

const toggleGroups = () => {
  showGroups.value = !showGroups.value
}

const toggleApplicantForm = () => {
  showApplicantForm.value = !showApplicantForm.value
}

const closeApplicantForm = () => {
  showApplicantForm.value = false
  currentTab.value = "Dashboard"
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}

const getExamEndTime = (exam) => {
  if (!exam.Exam_Date || !exam.Exam_Time || !exam.Duration_Minutes) return null
  const start = new Date(`${exam.Exam_Date}T${exam.Exam_Time}`)
  return new Date(start.getTime() + Number(exam.Duration_Minutes) * 60000)
}

const loadExamStatuses = async (exams) => {
  const statusMap = {}
  for (const exam of exams) {
    try {
      const res = await axios.get(`/exam/status/${exam.Exam_Id}`)
      statusMap[exam.Exam_Id] = res.data.success ? res.data.status : { has_question_bank: false, has_question_paper: false }
    } catch {
      statusMap[exam.Exam_Id] = { has_question_bank: false, has_question_paper: false }
    }
  }
  examStatus.value = statusMap
}

const fetchExamsAndCategorize = async () => {
  try {
    const res = await axios.get(`/exam/get_exams/${facultyEmail}`)
    if (res.data.success) {
      const now = new Date()
      const allExams = res.data.exams || []

      createdExams.value = allExams.filter(exam => now < getExamEndTime(exam))
      conductedExams.value = allExams.filter(exam => now >= getExamEndTime(exam))

      await loadExamStatuses(createdExams.value)
    }

    const conductedRes = await axios.get(`/faculty/conducted_exams/${facultyEmail}`)
    if (conductedRes.data.success) {
      conductedExams.value = conductedRes.data.exams
    }
  } catch (err) {
    console.error('Failed to fetch exams', err)
  }
}

const submitExam = async () => {
  try {
    const res = await axios.post('/exam/create', exam.value)
    if (res.data.success) {
      examSubmitMessage.value = 'Exam created successfully!'
      showForm.value = false
      fetchExamsAndCategorize()

      exam.value = {
        exam_name: '',
        exam_date: '',
        exam_time: '',
        duration: '',
        total_questions: '',
        max_marks: '',
        faculty_email: facultyEmail
      }
    } else {
      examSubmitMessage.value = res.data.message || 'Failed to create exam.'
    }
  } catch {
    examSubmitMessage.value = 'Error creating exam.'
  }
}

const deleteExam = async (examId) => {
  if (!confirm('Are you sure you want to delete this exam?')) return
  
  try {
    const res = await axios.delete(`/exam/delete/${examId}`)
    if (res.data.success) {
      fetchExamsAndCategorize()
    }
  } catch (err) {
    console.error('Failed to delete exam', err)
  }
}


const goToTab = (tab) => {
  activeTab.value = tab
}

const toggleRoleMenu = () => {
  showRoleMenu.value = !showRoleMenu.value
}

const selectRole = (roleId) => {
  if (roleId === 'admin') {
    localStorage.setItem("active_role", "Admin")
    showRoleMenu.value = false
    router.push('/admin?from=faculty')
  }
}

const logout = async () => {
  try {
    await axios.post('/auth/logout', {
      email,
      role: activeRole.value
    })

    localStorage.clear()
    router.push('/')
  } catch {
    alert('Logout failed. Try again.')
  }
}
</script>

<style scoped>
/* Prevent scrolling issues */
body, html {
  overflow-x: hidden;

.p-6 {
  padding: 1.5rem;
  background: transparent !important;
  min-height: 100vh;
  font-family: 'Inter', sans-serif;
}
h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  background: linear-gradient(to right, #2563eb, #4f46e5);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
button.bg-blue-600 {
  background: linear-gradient(to right, #2563eb, #4f46e5);
  padding: 0.5rem 1.25rem;
  border-radius: 1rem;
  font-weight: 600;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
button.bg-blue-600:hover {
  background: linear-gradient(to right, #1d4ed8, #4338ca);
  transform: scale(1.03);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
}

* {
  box-sizing: border-box;
}

.min-h-screen {
  overflow: hidden;
}

/* Icon container for consistent sizing */
.icon-container {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

/* Icon image styling */
.icon-image {
  width: 24px;
  height: 24px;
  object-fit: contain;
  display: block;
}
}

/* Icon container for consistent sizing */
.icon-container {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

/* Full-page gradient */
.container-wrapper {
  min-height: 100vh;
  padding: 1.5rem;
  background: linear-gradient(to bottom right, #E3F2FD, #F3E5F5, #FCE4EC);
  font-family: 'Inter', sans-serif;
}

/* Full-page gradient */
.container-wrapper {
  min-height: 100vh;
  padding: 1.5rem;
  background: linear-gradient(to bottom right, #E3F2FD, #F3E5F5, #FCE4EC);
  font-family: 'Inter', sans-serif;
}

</style>