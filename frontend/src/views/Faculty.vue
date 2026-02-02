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
        <div class="flex items-center justify-between w-full">

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
              class="w-10 h-10 flex items-center justify-center rounded-xl
                     bg-gradient-to-br from-blue-500 to-indigo-600
                     text-white shadow-md hover:shadow-lg transition shrink-0"
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

        </div>
      </div>

      <!-- Navigation Menu -->
      <nav class="flex-1 py-4 px-3 space-y-1.5">
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
      <div class="p-8 pt-1 max-w-full overflow-x-hidden"> 
        <!-- 🔔 Faculty Notification Bell -->
        <div class="flex justify-end mb-4">
          <div class="relative">

            <!-- 🔔 Bell Button -->
            <button
              @click="showNotifications = !showNotifications"
              class="w-11 h-11 bg-white rounded-full shadow-md
                     flex items-center justify-center hover:bg-gray-100 relative"
            >
              🔔
              <span
                v-if="upcomingFacultyExams.length"
                class="absolute -top-1 -right-1 bg-red-600 text-white
                       text-xs font-bold rounded-full px-1.5"
              >
                {{ upcomingFacultyExams.length }}
              </span>
            </button>

            <!-- Dropdown -->
            <div
              v-if="showNotifications"
              class="absolute right-0 mt-3 w-96 bg-white rounded-2xl
                     shadow-2xl z-[9999] overflow-hidden"
            >
              <!-- Header -->
              <div class="px-6 py-4 bg-gradient-to-r from-blue-50 to-indigo-50
                          flex justify-between items-center">
                <span class="font-bold text-gray-800">
                  🔔 Your Upcoming Exams
                </span>
                <span class="text-sm text-gray-500">
                  {{ upcomingFacultyExams.length }}
                </span>
              </div>

              <!-- Notifications -->
              <div
                v-if="upcomingFacultyExams.length"
                class="p-4 space-y-3 max-h-[420px] overflow-y-auto"
              >
                <div
                  v-for="exam in upcomingFacultyExams"
                  :key="exam.Exam_Id"
                  class="bg-gray-50 rounded-xl p-4
                         hover:bg-indigo-50 transition relative shadow-sm"
                >
                  <!-- Exam Name -->
                  <p class="font-semibold text-gray-800">
                    {{ exam.Exam_Name }}
                  </p>
                  <!-- ❌ Dismiss -->
                  <button
                    @click.stop="dismissExam(exam.Exam_Id)"
                    class="absolute top-3 right-3 text-gray-400
                           hover:text-red-600 text-lg font-bold"
                    title="Dismiss"
                  >
                    ×
                  </button>

                  <!-- Date & Time -->
                  <p class="text-sm text-gray-500 mt-1">
                    📅 {{ exam.Exam_Date }} • ⏰ {{ exam.Exam_Time }}
                  </p>

                  <!-- 🔴 Starting Soon -->
                  <span
                    v-if="isStartingSoon(exam)"
                    class="inline-block mt-2 bg-red-100 text-red-600
                           px-3 py-1 rounded-full text-xs font-semibold"
                  >
                    ⏳ Starting in {{ formatCountdown(exam) }}
                  </span>

                  <!-- 🟢 Upcoming -->
                  <span
                    v-else
                    class="inline-block mt-2 bg-green-100 text-green-600
                           px-3 py-1 rounded-full text-xs font-semibold"
                  >
                    📌 Upcoming
                  </span>
                </div>
              </div>

              <!-- Empty -->
              <div v-else class="px-6 py-8 text-sm text-gray-500 text-center">
                <div class="text-3xl mb-2">🎉</div>
                No upcoming exams
              </div>
            </div>

          </div>
        </div>

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
              <!-- Created Exams Table -->
              <div v-if="createdExams.length" class="mt-8">
                <h2 class="text-2xl font-semibold mb-4 text-gray-800">Created Exams</h2>
                <div class="bg-white rounded-xl shadow-lg overflow-hidden">
                  <table class="min-w-full">
                    <thead class="bg-gradient-to-r from-blue-50 to-indigo-50">
                      <tr>
                        <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Exam Name</th>
                        <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Date</th>
                        <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Time</th>
                        <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Duration</th>
                        <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Questions</th>
                        <th class="px-6 py-4 text-left text-sm font-bold text-gray-700">Max Marks</th>
                        <th class="px-6 py-4 text-center text-sm font-bold text-gray-700">Actions</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200">
                      <tr v-for="exam in createdExams" :key="exam.Exam_Id" class="hover:bg-gray-50 transition">
                        <td class="px-6 py-4 text-sm text-gray-800 font-medium">{{ exam.Exam_Name }}</td>
                        <td class="px-6 py-4 text-sm text-gray-600">{{ exam.Exam_Date }}</td>
                        <td class="px-6 py-4 text-sm text-gray-600">{{ exam.Exam_Time }}</td>
                        <td class="px-6 py-4 text-sm text-gray-600">{{ exam.Duration_Minutes }} min</td>
                        <td class="px-6 py-4 text-sm text-gray-600">{{ exam.Total_Questions }}</td>
                        <td class="px-6 py-4 text-sm text-gray-600">{{ exam.Max_Marks }}</td>
                        <td class="px-6 py-4">  
                          <div class="flex flex-wrap justify-center items-center gap-2">

                            <!-- Add Students -->
                            <button
                              @click.stop="addStudents(exam.Exam_Id)"
                              class="flex items-center gap-1 bg-blue-400 hover:bg-blue-500 text-white px-3 py-1.5 rounded-full text-xs font-semibold shadow hover:scale-105 transition-all duration-200"
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
                      <tr v-for="exam in paginatedConductedExams" :key="exam.Exam_Id" class="hover:bg-gray-50 transition">
                        <td class="px-6 py-4 text-sm text-gray-800 font-medium">{{ exam.Exam_Name || 'N/A' }}</td>
                        <td class="px-6 py-4 text-sm text-gray-600">{{ formatDate(exam.Exam_Date) }}</td>
                        <td class="px-6 py-4 text-sm text-gray-600">{{ exam.total_applicants || 0 }}</td>
                        <td class="px-6 py-4 text-sm text-gray-600">{{ exam.attempted_applicants || 0 }}</td>
                        <td class="px-6 py-4 text-center">
                          <button
                            @click="navigateTo('ViewResponsesFaculty', exam.Exam_Id)"
                            class="bg-purple-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-purple-700 shadow-md hover:shadow-lg transition font-semibold"
                          >
                            View Responses
                          </button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>

                <!-- Pagination for Conducted Exams -->
                <div v-if="conductedExams.length > 0" class="bg-gray-50 px-6 py-4 border-t border-gray-200">
                  <div class="flex items-center justify-between">
                    
                    <!-- Results Info -->
                    <div class="text-sm text-gray-700">
                      Showing 
                      <span class="font-semibold">{{ conductedStartIndex + 1 }}</span>
                      to 
                      <span class="font-semibold">{{ conductedEndIndex }}</span>
                      of 
                      <span class="font-semibold">{{ totalConductedExams }}</span>
                      results
                    </div>

                    <!-- Pagination Buttons -->
                    <div class="flex items-center gap-2">
                      
                      <!-- Previous Button -->
                      <button
                        @click="goToConductedPage(currentConductedPage - 1)"
                        :disabled="currentConductedPage === 1"
                        class="px-3 py-2 rounded-lg border border-gray-300 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
                      >
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
                        </svg>
                      </button>

                      <!-- Page Numbers -->
                      <button
                        v-for="page in totalConductedPages"
                        :key="page"
                        @click="goToConductedPage(page)"
                        class="px-4 py-2 rounded-lg border transition"
                        :class="currentConductedPage === page 
                          ? 'bg-blue-600 text-white border-blue-600' 
                          : 'border-gray-300 bg-white hover:bg-gray-50'"
                      >
                        {{ page }}
                      </button>

                      <!-- Next Button -->
                      <button
                        @click="goToConductedPage(currentConductedPage + 1)"
                        :disabled="currentConductedPage === totalConductedPages"
                        class="px-3 py-2 rounded-lg border border-gray-300 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
                      >
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                        </svg>
                      </button>

                    </div>
                  </div>
                </div>
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
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from '../utils/axiosInstance'
import FacultyGroups from "../views/Groups.vue"
import AddApplicantsPage from "../views/AddApplicantsPage.vue"
import UploadStudents from './UploadStudents.vue'
import Groups from './Groups.vue'

const now = ref(new Date())
let countdownTimer = null
const router = useRouter()

/* ================= AUTH ================= */
const roles = JSON.parse(localStorage.getItem("roles") || "[]")
const activeRole = ref(localStorage.getItem("active_role"))
const canSwitch = roles.includes("Admin") && roles.includes("Faculty")

/* ================= FACULTY INFO ================= */
const facultyName = ref(localStorage.getItem("name") || "Faculty")
const facultyInitial = computed(() => facultyName.value.charAt(0).toUpperCase())
const email = localStorage.getItem("email")
const facultyEmail = email

/* ================= 🔔 FACULTY NOTIFICATIONS ================= */
const showNotifications = ref(false)
const dismissedExamIds = ref(new Set())

const dismissExam = (examId) => {
  dismissedExamIds.value.add(examId)
}

const upcomingFacultyExams = computed(() => {
  return createdExams.value.filter(exam => {
    const examDateTime = new Date(`${exam.Exam_Date}T${exam.Exam_Time}`)
    return (
      examDateTime > now.value &&
      !dismissedExamIds.value.has(exam.Exam_Id)
    )
  })
})

const getRemainingSeconds = (exam) => {
  const examTime = new Date(`${exam.Exam_Date}T${exam.Exam_Time}`)
  return Math.floor((examTime - now.value) / 1000)
}

const isStartingSoon = (exam) => {
  const secs = getRemainingSeconds(exam)
  return secs > 0 && secs <= 600
}

const formatCountdown = (exam) => {
  const secs = getRemainingSeconds(exam)
  if (secs <= 0) return "Starting now"
  const m = Math.floor(secs / 60)
  const s = secs % 60
  return `${m}m ${s}s`
}

/* ================= UI STATE ================= */
const sidebarOpen = ref(true)
const showRoleMenu = ref(false)
const activeTab = ref(null)
const currentTab = ref("Dashboard")

/* ================= TABS ================= */
const allTabs = [
  { id: "my-exams", name: "My Exams", icon: "exams", access: "create_exam" },
  { id: "groups", name: "Groups", icon: "groups", access: "view_groups" },
  { id: "add-applicants", name: "Add Students", icon: "applicants", access: "add_applicants" },
  { id: "upload-students", name: "Upload Students", icon: "applicants", access: "upload_students" }
]

const facultyPermissions = ref({
  create_exam: true,
  view_groups: true,
  add_applicants: true,
  upload_students: true
})

const visibleTabs = computed(() =>
  allTabs.filter(tab => facultyPermissions.value[tab.access])
)

/* ================= EXAM DATA ================= */
const showForm = ref(false)
const examSubmitMessage = ref('')
const createdExams = ref([])
const conductedExams = ref([])
const examStatus = ref({})
const showGroups = ref(false)
const showApplicantForm = ref(false)

const todayDate = computed(() => {
  const d = new Date()
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
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

/* ================= PAGINATION STATE ================= */
const itemsPerPage = ref(15)

// Conducted Exams Pagination
const currentConductedPage = ref(1)

/* ================= CONDUCTED EXAMS PAGINATION ================= */
const totalConductedExams = computed(() => conductedExams.value.length)
const totalConductedPages = computed(() =>
  Math.ceil(totalConductedExams.value / itemsPerPage.value)
)

const paginatedConductedExams = computed(() => {
  const start = (currentConductedPage.value - 1) * itemsPerPage.value
  return conductedExams.value.slice(start, start + itemsPerPage.value)
})

const conductedStartIndex = computed(() =>
  (currentConductedPage.value - 1) * itemsPerPage.value
)

const conductedEndIndex = computed(() => {
  const end = currentConductedPage.value * itemsPerPage.value
  return end > totalConductedExams.value ? totalConductedExams.value : end
})

const goToConductedPage = (page) => {
  if (page >= 1 && page <= totalConductedPages.value) {
    currentConductedPage.value = page
    window.scrollTo({ top: 0, behavior: "smooth" })
  }
}

/* ================= LIFECYCLE ================= */
onMounted(() => {
  if (activeRole.value !== "Faculty") {
    router.push("/")
    return
  }

  fetchExamsAndCategorize()

  // ⏱ realtime clock
  countdownTimer = setInterval(() => {
    now.value = new Date()
  }, 1000)

  activeTab.value = 'my-exams'
})

onUnmounted(() => {
  if (countdownTimer) clearInterval(countdownTimer)
})

/* ================= METHODS ================= */
const toggleExamForm = () => {
  showForm.value = !showForm.value
  examSubmitMessage.value = ''
}

const goToTab = (tab) => {
  activeTab.value = tab
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
      statusMap[exam.Exam_Id] = res.data.success
        ? res.data.status
        : { has_question_bank: false, has_question_paper: false }
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
      const exams = res.data.exams || []

      createdExams.value = exams.filter(e => now < getExamEndTime(e))
      conductedExams.value = exams.filter(e => now >= getExamEndTime(e))

      await loadExamStatuses(createdExams.value)
    }
  } catch (err) {
    console.error("Failed to fetch exams", err)
  }
}

const submitExam = async () => {
  try {
    const res = await axios.post('/exam/create', exam.value)
    if (res.data.success) {
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
      examSubmitMessage.value = res.data.message || 'Failed to create exam'
    }
  } catch {
    examSubmitMessage.value = 'Error creating exam'
  }
}

const deleteExam = async (examId) => {
  if (!confirm("Delete this exam?")) return

  try {
    const res = await axios.delete(
      `/faculty/exam/delete/${examId}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`
        }
      }
    )

    if (res.data.success) {
      fetchExamsAndCategorize()
    } else {
      alert(res.data.message || "Failed to delete exam")
    }

  } catch (err) {
    console.error("Delete failed", err)
    alert("Delete failed. Check console.")
  }
}

/* ================= ✅ FIXED ADD STUDENTS ================= */
const addStudents = (examId) => {
  console.log("Add Students clicked for exam:", examId)

  if (!examId) {
    alert("Invalid exam ID")
    return
  }

  router.push({
    name: 'AddApplicantsExam',
    params: { examId }
  })
}

/* ================= ✅ NAVIGATION HELPER ================= */
const navigateTo = (routeName, examId) => {
  console.log("Navigating to:", routeName, examId)

  if (!examId) {
    alert("Invalid exam ID")
    return
  }

  router.push({
    name: routeName,
    params: { examId }
  })
}

/* ================= ROLE SWITCH ================= */
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
    alert('Logout failed')
  }
}
</script>

<style scoped>
/* Prevent scrolling issues */
body, html {
  overflow-x: hidden;
}

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

/* Full-page gradient */
.container-wrapper {
  min-height: 100vh;
  padding: 1.5rem;
  background: linear-gradient(to bottom right, #E3F2FD, #F3E5F5, #FCE4EC);
  font-family: 'Inter', sans-serif;
}

/* Smooth transitions for pagination buttons */
button {
  transition: all 0.2s ease;
}

button:hover:not(:disabled) {
  transform: translateY(-1px);
}

button:active:not(:disabled) {
  transform: translateY(0);
}
</style>