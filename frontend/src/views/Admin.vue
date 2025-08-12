<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-100 to-pink-100">
    <!-- Header -->
    <div class="px-6 py-6">
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-4xl font-bold text-blue-600">Welcome, {{ adminName }}</h1>
        <button
          @click="logout"
          class="bg-red-500 hover:bg-red-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all duration-200 transform hover:scale-105"
        >
          Logout
        </button>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-wrap gap-4 mb-8">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="[
            'px-6 py-3 rounded-full font-semibold shadow-lg transition-all duration-200 transform hover:scale-105',
            activeTab === tab.id
              ? 'bg-blue-600 text-white'
              : 'bg-blue-500 hover:bg-blue-600 text-white'
          ]"
        >
          {{ tab.name }}
        </button>
      </div>

      <!-- Error/Success Messages -->
      <div v-if="message" class="mb-6 p-4 rounded-xl shadow-lg" :class="messageType === 'error' ? 'bg-red-100 text-red-700 border border-red-200' : 'bg-green-100 text-green-700 border border-green-200'">
        {{ message }}
        <button @click="message = ''" class="float-right text-lg font-bold hover:opacity-70">&times;</button>
      </div>

      <!-- Faculty Management -->
      <div v-if="activeTab === 'faculty'" class="space-y-6">
        <div class="bg-white/80 backdrop-blur-sm shadow-xl rounded-2xl p-8 border border-white/20">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-800">Faculty Management</h2>
            <button
              @click="showAddFacultyModal = true"
              class="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all duration-200 transform hover:scale-105"
            >
              Add Faculty
            </button>
          </div>

          <!-- Faculty Table -->
          <div class="bg-blue-50/50 rounded-xl p-6 border border-blue-100">
            <div class="overflow-x-auto">
              <table class="w-full">
                <thead>
                  <tr class="border-b border-blue-200">
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">ID</th>
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">Name</th>
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">Email</th>
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">School</th>
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">Designation</th>
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="faculty in facultyList" :key="faculty.Faculty_Id" class="border-b border-blue-100 hover:bg-blue-50/50">
                    <td class="py-4 px-4 text-gray-700">{{ faculty.Faculty_Id }}</td>
                    <td class="py-4 px-4 text-gray-700">{{ faculty.F_Name }}</td>
                    <td class="py-4 px-4 text-gray-700">{{ faculty.F_Email }}</td>
                    <td class="py-4 px-4 text-gray-700">{{ getSchoolName(faculty.School_Id) }}</td>
                    <td class="py-4 px-4 text-gray-700">{{ faculty.Designation }}</td>
                    <td class="py-4 px-4 space-x-2">
                      <button
                        @click="editFaculty(faculty)"
                        class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 transform hover:scale-105"
                      >
                        Edit
                      </button>
                      <button
                        @click="deleteFaculty(faculty.Faculty_Id)"
                        class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 transform hover:scale-105"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Schools Management -->
      <div v-if="activeTab === 'schools'" class="space-y-6">
        <div class="bg-white/80 backdrop-blur-sm shadow-xl rounded-2xl p-8 border border-white/20">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-800">Schools Management</h2>
            <button
              @click="showAddSchoolModal = true"
              class="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all duration-200 transform hover:scale-105"
            >
              Add School
            </button>
          </div>

          <!-- Schools Table -->
          <div class="bg-blue-50/50 rounded-xl p-6 border border-blue-100">
            <div class="overflow-x-auto">
              <table class="w-full">
                <thead>
                  <tr class="border-b border-blue-200">
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">ID</th>
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">School Name</th>
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">Short Name</th>
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="school in schoolsList" :key="school.School_Id" class="border-b border-blue-100 hover:bg-blue-50/50">
                    <td class="py-4 px-4 text-gray-700">{{ school.School_Id }}</td>
                    <td class="py-4 px-4 text-gray-700">{{ school.School_Name }}</td>
                    <td class="py-4 px-4 text-gray-700">{{ school.School_Short }}</td>
                    <td class="py-4 px-4 space-x-2">
                      <button
                        @click="editSchool(school)"
                        class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 transform hover:scale-105"
                      >
                        Edit
                      </button>
                      <button
                        @click="deleteSchool(school.School_Id)"
                        class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 transform hover:scale-105"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Applicants Management -->
      <div v-if="activeTab === 'applicants'" class="space-y-6">
        <!-- Action Buttons -->
        <div class="flex gap-4 mb-6">
          <button
            @click="showAddApplicantForm = !showAddApplicantForm"
            class="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all duration-200 transform hover:scale-105"
          >
            {{ showAddApplicantForm ? 'Close' : 'Add Applicants' }}
          </button>
          <button
            @click="showUploadApplicantsModal = true"
            class="bg-purple-500 hover:bg-purple-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all duration-200 transform hover:scale-105"
          >
            Upload Applicants
          </button>
        </div>

        <!-- Add Applicant Form -->
        <div v-if="showAddApplicantForm" class="bg-white/80 backdrop-blur-sm shadow-xl rounded-2xl p-8 border border-white/20 mb-6">
          <h3 class="text-2xl font-bold text-gray-800 mb-6">Add New Applicant</h3>
          <form @submit.prevent="submitApplicant">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Full Name</label>
                <input
                  v-model="newApplicant.Full_Name"
                  type="text"
                  required
                  class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
                  placeholder="Enter full name"
                >
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Email</label>
                <input
                  v-model="newApplicant.Email"
                  type="email"
                  required
                  class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
                  placeholder="Enter email address"
                >
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Password</label>
                <input
                  v-model="newApplicant.Password"
                  type="password"
                  required
                  class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
                  placeholder="Enter password"
                >
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Phone</label>
                <input
                  v-model="newApplicant.Phone"
                  type="tel"
                  class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
                  placeholder="Enter phone number"
                >
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Date of Birth</label>
                <input
                  v-model="newApplicant.DOB"
                  type="date"
                  class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
                >
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Gender</label>
                <select
                  v-model="newApplicant.Gender"
                  class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
                >
                  <option value="">Select Gender</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-semibold text-gray-700 mb-2">Address</label>
                <textarea
                  v-model="newApplicant.Address"
                  rows="3"
                  class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
                  placeholder="Enter address"
                ></textarea>
              </div>
            </div>
            <div class="flex justify-end space-x-4 mt-8">
              <button
                type="button"
                @click="showAddApplicantForm = false"
                class="px-6 py-3 text-sm font-semibold text-gray-700 bg-gray-200 hover:bg-gray-300 rounded-full transition-all duration-200 transform hover:scale-105"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="px-6 py-3 text-sm font-semibold text-white bg-blue-500 hover:bg-blue-600 rounded-full transition-all duration-200 transform hover:scale-105"
              >
                Add Applicant
              </button>
            </div>
          </form>
        </div>

        <!-- Applicants Table -->
        <div class="bg-white/80 backdrop-blur-sm shadow-xl rounded-2xl border border-white/20">
          <div class="flex justify-between items-center p-8 border-b border-gray-200">
            <h2 class="text-2xl font-bold text-gray-800">Applicants Management</h2>
            <div class="space-x-2">
              <button
                v-if="selectedApplicants.length > 0"
                @click="bulkDeleteApplicants"
                class="bg-red-500 hover:bg-red-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all duration-200 transform hover:scale-105"
              >
                Delete Selected ({{ selectedApplicants.length }})
              </button>
            </div>
          </div>

          <!-- Applicants Table -->
          <div class="bg-blue-50/50 rounded-b-2xl p-6">
            <div class="overflow-x-auto">
              <table class="w-full">
                <thead>
                  <tr class="border-b border-blue-200">
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">
                      <input 
                        type="checkbox" 
                        @change="toggleAllApplicants"
                        :checked="selectedApplicants.length === applicantsList.length && applicantsList.length > 0"
                        class="rounded border-blue-300 text-blue-600 focus:ring-blue-500"
                      >
                    </th>
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">ID</th>
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">Name</th>
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">Email</th>
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">Phone</th>
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">Gender</th>
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">Registration Date</th>
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="applicant in applicantsList" :key="applicant.Applicant_Id" class="border-b border-blue-100 hover:bg-blue-50/50">
                    <td class="py-4 px-4">
                      <input 
                        type="checkbox" 
                        :value="applicant.Applicant_Id"
                        v-model="selectedApplicants"
                        class="rounded border-blue-300 text-blue-600 focus:ring-blue-500"
                      >
                    </td>
                    <td class="py-4 px-4 text-gray-700">{{ applicant.Applicant_Id }}</td>
                    <td class="py-4 px-4 text-gray-700">{{ applicant.Full_Name }}</td>
                    <td class="py-4 px-4 text-gray-700">{{ applicant.Email }}</td>
                    <td class="py-4 px-4 text-gray-700">{{ applicant.Phone }}</td>
                    <td class="py-4 px-4 text-gray-700">{{ applicant.Gender }}</td>
                    <td class="py-4 px-4 text-gray-700">{{ formatDate(applicant.Registration_Date) }}</td>
                    <td class="py-4 px-4 space-x-2">
                      <button
                        @click="viewApplicant(applicant)"
                        class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 transform hover:scale-105"
                      >
                        View
                      </button>
                      <button
                        @click="deleteApplicant(applicant.Applicant_Id)"
                        class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 transform hover:scale-105"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-if="applicantsList.length === 0" class="text-center py-12 text-gray-500">
              No applicants found. Add some applicants to get started.
            </div>
          </div>
        </div>
      </div>

      <!-- Admins Management -->
      <div v-if="activeTab === 'admins'" class="space-y-6">
        <div class="bg-white/80 backdrop-blur-sm shadow-xl rounded-2xl p-8 border border-white/20">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-800">Admins Management</h2>
            <button
              @click="showAddAdminModal = true"
              class="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6 py-3 rounded-full shadow-lg transition-all duration-200 transform hover:scale-105"
            >
              Add Admin
            </button>
          </div>

          <div class="bg-blue-50/50 rounded-xl p-6 border border-blue-100">
            <div class="overflow-x-auto">
              <table class="w-full">
                <thead>
                  <tr class="border-b border-blue-200">
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">ID</th>
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">Name</th>
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">Email</th>
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="admin in adminsList" :key="admin.Admin_ID" class="border-b border-blue-100 hover:bg-blue-50/50">
                    <td class="py-4 px-4 text-gray-700">{{ admin.Admin_ID }}</td>
                    <td class="py-4 px-4 text-gray-700">{{ admin.Name }}</td>
                    <td class="py-4 px-4 text-gray-700">{{ admin.Email }}</td>
                    <td class="py-4 px-4 space-x-2">
                      <button @click="editAdmin(admin)" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 transform hover:scale-105">Edit</button>
                      <button @click="deleteAdmin(admin.Admin_ID)" class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 transform hover:scale-105">Delete</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Login Logs Management -->
      <div v-if="activeTab === 'logs'" class="space-y-6">
        <div class="bg-white/80 backdrop-blur-sm shadow-xl rounded-2xl p-8 border border-white/20">
          <h2 class="text-2xl font-bold text-gray-800 mb-6">Login Logs</h2>

          <div class="bg-blue-50/50 rounded-xl p-6 border border-blue-100">
            <div class="overflow-x-auto">
              <table class="w-full">
                <thead>
                  <tr class="border-b border-blue-200">
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">Log ID</th>
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">User Email</th>
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">Role</th>
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">Login Time</th>
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">Logout Time</th>
                    <th class="text-left py-4 px-4 font-semibold text-blue-800">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="log in logsList" :key="log.Log_ID" class="border-b border-blue-100 hover:bg-blue-50/50">
                    <td class="py-4 px-4 text-gray-700">{{ log.Log_ID }}</td>
                    <td class="py-4 px-4 text-gray-700">{{ log.User_Email }}</td>
                    <td class="py-4 px-4">
                      <span :class="getRoleColor(log.Role)" class="px-3 py-1 rounded-full text-xs font-medium">
                        {{ log.Role }}
                      </span>
                    </td>
                    <td class="py-4 px-4 text-gray-700">{{ formatDateTime(log.Login_Time) }}</td>
                    <td class="py-4 px-4 text-gray-700">{{ formatDateTime(log.Logout_Time) }}</td>
                    <td class="py-4 px-4 space-x-2">
                      <button @click="viewLog(log)" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 transform hover:scale-105">View</button>
                      <button @click="deleteLog(log.Log_ID)" class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 transform hover:scale-105">Delete</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- All modals with updated styling -->
    <!-- Add/Edit Faculty Modal -->
    <div v-if="showAddFacultyModal || showEditFacultyModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm overflow-y-auto h-full w-full z-50 flex items-center justify-center">
      <div class="bg-white/90 backdrop-blur-sm shadow-2xl rounded-2xl p-8 w-96 border border-white/20">
        <h3 class="text-2xl font-bold text-gray-800 mb-6">
          {{ showAddFacultyModal ? 'Add Faculty' : 'Edit Faculty' }}
        </h3>
        <form @submit.prevent="showAddFacultyModal ? addFaculty() : updateFaculty()">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Name</label>
              <input
                v-model="facultyForm.F_Name"
                type="text"
                required
                class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
              >
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Email</label>
              <input
                v-model="facultyForm.F_Email"
                type="email"
                required
                class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
              >
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">School</label>
              <select
                v-model="facultyForm.School_Id"
                required
                class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
              >
                <option value="">Select School</option>
                <option v-for="school in schoolsList" :key="school.School_Id" :value="school.School_Id">
                  {{ school.School_Name }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Designation</label>
              <input
                v-model="facultyForm.Designation"
                type="text"
                required
                class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
              >
            </div>
            <div v-if="showAddFacultyModal">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Password</label>
              <input
                v-model="facultyForm.Password"
                type="password"
                required
                class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
              >
            </div>
          </div>
          <div class="flex justify-end space-x-4 mt-8">
            <button
              type="button"
              @click="closeFacultyModal"
              class="px-6 py-3 text-sm font-semibold text-gray-700 bg-gray-200 hover:bg-gray-300 rounded-full transition-all duration-200 transform hover:scale-105"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-6 py-3 text-sm font-semibold text-white bg-blue-500 hover:bg-blue-600 rounded-full transition-all duration-200 transform hover:scale-105"
            >
              {{ showAddFacultyModal ? 'Add' : 'Update' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Add/Edit School Modal -->
    <div v-if="showAddSchoolModal || showEditSchoolModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm overflow-y-auto h-full w-full z-50 flex items-center justify-center">
      <div class="bg-white/90 backdrop-blur-sm shadow-2xl rounded-2xl p-8 w-96 border border-white/20">
        <h3 class="text-2xl font-bold text-gray-800 mb-6">
          {{ showAddSchoolModal ? 'Add School' : 'Edit School' }}
        </h3>
        <form @submit.prevent="showAddSchoolModal ? addSchool() : updateSchool()">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">School Name</label>
              <input
                v-model="schoolForm.School_Name"
                type="text"
                required
                class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
              >
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Short Name</label>
              <input
                v-model="schoolForm.School_Short"
                type="text"
                required
                class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
              >
            </div>
          </div>
          <div class="flex justify-end space-x-4 mt-8">
            <button
              type="button"
              @click="closeSchoolModal"
              class="px-6 py-3 text-sm font-semibold text-gray-700 bg-gray-200 hover:bg-gray-300 rounded-full transition-all duration-200 transform hover:scale-105"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-6 py-3 text-sm font-semibold text-white bg-blue-500 hover:bg-blue-600 rounded-full transition-all duration-200 transform hover:scale-105"
            >
              {{ showAddSchoolModal ? 'Add' : 'Update' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- View Applicant Modal -->
    <div v-if="showViewApplicantModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm overflow-y-auto h-full w-full z-50 flex items-center justify-center">
      <div class="bg-white/90 backdrop-blur-sm shadow-2xl rounded-2xl p-8 w-96 border border-white/20">
        <h3 class="text-2xl font-bold text-gray-800 mb-6">Applicant Details</h3>
        <div v-if="selectedApplicant" class="space-y-4">
          <div class="flex justify-between"><span class="font-semibold">Name:</span> <span>{{ selectedApplicant.Full_Name }}</span></div>
          <div class="flex justify-between"><span class="font-semibold">Email:</span> <span>{{ selectedApplicant.Email }}</span></div>
          <div class="flex justify-between"><span class="font-semibold">Phone:</span> <span>{{ selectedApplicant.Phone }}</span></div>
          <div class="flex justify-between"><span class="font-semibold">DOB:</span> <span>{{ formatDate(selectedApplicant.DOB) }}</span></div>
          <div class="flex justify-between"><span class="font-semibold">Gender:</span> <span>{{ selectedApplicant.Gender }}</span></div>
          <div class="flex justify-between"><span class="font-semibold">Address:</span> <span>{{ selectedApplicant.Address }}</span></div>
          <div class="flex justify-between"><span class="font-semibold">Registration Date:</span> <span>{{ formatDate(selectedApplicant.Registration_Date) }}</span></div>
        </div>
        <div class="flex justify-end mt-8">
          <button
            @click="showViewApplicantModal = false"
            class="px-6 py-3 text-sm font-semibold text-gray-700 bg-gray-200 hover:bg-gray-300 rounded-full transition-all duration-200 transform hover:scale-105"
          >
            Close
          </button>
        </div>
      </div>
    </div>

    <!-- Add/Edit Admin Modal -->
    <div v-if="showAddAdminModal || showEditAdminModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm overflow-y-auto h-full w-full z-50 flex items-center justify-center">
      <div class="bg-white/90 backdrop-blur-sm shadow-2xl rounded-2xl p-8 w-96 border border-white/20">
        <h3 class="text-2xl font-bold text-gray-800 mb-6">
          {{ showAddAdminModal ? 'Add Admin' : 'Edit Admin' }}
        </h3>
        <form @submit.prevent="showAddAdminModal ? addAdmin() : updateAdmin()">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Name</label>
              <input v-model="adminForm.Name" type="text" required class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200">
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Email</label>
              <input v-model="adminForm.Email" type="email" required class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200">
            </div>
            <div v-if="showAddAdminModal">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Password</label>
              <input v-model="adminForm.Password" type="password" required class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200">
            </div>
          </div>
          <div class="flex justify-end space-x-4 mt-8">
            <button type="button" @click="closeAdminModal" class="px-6 py-3 text-sm font-semibold text-gray-700 bg-gray-200 hover:bg-gray-300 rounded-full transition-all duration-200 transform hover:scale-105">Cancel</button>
            <button type="submit" class="px-6 py-3 text-sm font-semibold text-white bg-blue-500 hover:bg-blue-600 rounded-full transition-all duration-200 transform hover:scale-105">
              {{ showAddAdminModal ? 'Add' : 'Update' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- View Log Modal -->
    <div v-if="showViewLogModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm overflow-y-auto h-full w-full z-50 flex items-center justify-center">
      <div class="bg-white/90 backdrop-blur-sm shadow-2xl rounded-2xl p-8 w-96 border border-white/20">
        <h3 class="text-2xl font-bold text-gray-800 mb-6">Login Log Details</h3>
        <div v-if="selectedLog" class="space-y-4">
          <div class="flex justify-between"><span class="font-semibold">Log ID:</span> <span>{{ selectedLog.Log_ID }}</span></div>
          <div class="flex justify-between"><span class="font-semibold">User Email:</span> <span>{{ selectedLog.User_Email }}</span></div>
          <div class="flex justify-between"><span class="font-semibold">Role:</span> <span>{{ selectedLog.Role }}</span></div>
          <div class="flex justify-between"><span class="font-semibold">Login Time:</span> <span>{{ formatDateTime(selectedLog.Login_Time) }}</span></div>
          <div class="flex justify-between"><span class="font-semibold">Logout Time:</span> <span>{{ formatDateTime(selectedLog.Logout_Time) }}</span></div>
          <div v-if="selectedLog.Student_ID" class="flex justify-between"><span class="font-semibold">Student ID:</span> <span>{{ selectedLog.Student_ID }}</span></div>
          <div v-if="selectedLog.Student_Name" class="flex justify-between"><span class="font-semibold">Student Name:</span> <span>{{ selectedLog.Student_Name }}</span></div>
          <div v-if="selectedLog.Applicant_ID" class="flex justify-between"><span class="font-semibold">Applicant ID:</span> <span>{{ selectedLog.Applicant_ID }}</span></div>
        </div>
        <div class="flex justify-end mt-8">
          <button @click="showViewLogModal = false" class="px-6 py-3 text-sm font-semibold text-gray-700 bg-gray-200 hover:bg-gray-300 rounded-full transition-all duration-200 transform hover:scale-105">Close</button>
        </div>
      </div>
    </div>

    <!-- Upload Applicants Modal -->
    <div v-if="showUploadApplicantsModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm overflow-y-auto h-full w-full z-50 flex items-center justify-center">
      <div class="bg-white/90 backdrop-blur-sm shadow-2xl rounded-2xl p-8 w-96 border border-white/20">
        <h3 class="text-2xl font-bold text-gray-800 mb-6">Upload Applicants</h3>
        
        <!-- File Upload Section -->
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">
              Select CSV/Excel File
            </label>
            <input
              ref="fileInput"
              type="file"
              accept=".csv,.xlsx,.xls"
              @change="handleFileSelect"
              class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            >
          </div>
          
          <!-- Sample Format -->
          <div class="bg-blue-50 p-4 rounded-xl border border-blue-200">
            <p class="text-sm font-semibold text-gray-700 mb-2">Expected CSV Format:</p>
            <code class="text-xs text-gray-600">
              Full_Name,Email,Password,Phone,DOB,Gender,Address<br>
              John Doe,john@example.com,password123,1234567890,1990-01-01,Male,123 Street
            </code>
          </div>
          
          <!-- Upload Progress -->
          <div v-if="uploadProgress > 0" class="w-full bg-gray-200 rounded-full h-3">
            <div 
              class="bg-blue-600 h-3 rounded-full transition-all duration-300" 
              :style="{ width: uploadProgress + '%' }"
            ></div>
          </div>
          
          <!-- Upload Results -->
          <div v-if="uploadResults" class="space-y-2">
            <div v-if="uploadResults.success > 0" class="text-green-600 text-sm font-medium">
              ✅ Successfully uploaded: {{ uploadResults.success }} applicants
            </div>
            <div v-if="uploadResults.errors.length > 0" class="text-red-600 text-sm font-medium">
              ❌ Errors: {{ uploadResults.errors.length }}
              <ul class="list-disc list-inside mt-1 max-h-20 overflow-y-auto">
                <li v-for="error in uploadResults.errors.slice(0, 5)" :key="error" class="text-xs">
                  {{ error }}
                </li>
                <li v-if="uploadResults.errors.length > 5" class="text-xs">
                  ... and {{ uploadResults.errors.length - 5 }} more errors
                </li>
              </ul>
            </div>
          </div>
        </div>
        
        <div class="flex justify-end space-x-4 mt-8">
          <button
            type="button"
            @click="closeUploadModal"
            class="px-6 py-3 text-sm font-semibold text-gray-700 bg-gray-200 hover:bg-gray-300 rounded-full transition-all duration-200 transform hover:scale-105"
          >
            Close
          </button>
          <button
            @click="uploadApplicants"
            :disabled="!selectedFile || isUploading"
            class="px-6 py-3 text-sm font-semibold text-white bg-purple-500 hover:bg-purple-600 disabled:bg-gray-400 rounded-full transition-all duration-200 transform hover:scale-105"
          >
            {{ isUploading ? 'Uploading...' : 'Upload' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// Data
const activeTab = ref('faculty')
const facultyList = ref([])
const schoolsList = ref([])
const applicantsList = ref([])
const adminsList = ref([])
const logsList = ref([])

// Message system
const message = ref('')
const messageType = ref('success')

// Selection for bulk operations
const selectedApplicants = ref([])

// Modals
const showAddFacultyModal = ref(false)
const showEditFacultyModal = ref(false)
const showAddSchoolModal = ref(false)
const showEditSchoolModal = ref(false)
const showViewApplicantModal = ref(false)
const showAddAdminModal = ref(false)
const showEditAdminModal = ref(false)
const showViewLogModal = ref(false)

// Forms
const facultyForm = ref({
  Faculty_Id: null,
  F_Name: '',
  F_Email: '',
  School_Id: '',
  Designation: '',
  Password: ''
})

const schoolForm = ref({
  School_Id: null,
  School_Name: '',
  School_Short: ''
})

const adminForm = ref({
  Admin_ID: null,
  Name: '',
  Email: '',
  Password: ''
})

const selectedApplicant = ref(null)
const selectedLog = ref(null)

// Add these new reactive variables
const showAddApplicantForm = ref(false)
const showUploadApplicantsModal = ref(false)
const selectedFile = ref(null)
const isUploading = ref(false)
const uploadProgress = ref(0)
const uploadResults = ref(null)

const newApplicant = ref({
  Full_Name: '',
  Email: '',
  Password: '',
  Phone: '',
  DOB: '',
  Gender: '',
  Address: ''
})

// Admin user info
const adminName = ref('Admin')
const adminEmail = ref(localStorage.getItem('faculty_email') || '') // Reuse same key as mentioned in the code

// Tabs
const tabs = [
  { id: 'faculty', name: 'Faculty' },
  { id: 'schools', name: 'Schools' },
  { id: 'applicants', name: 'Applicants' },
  { id: 'admins', name: 'Admins' },
  { id: 'logs', name: 'Login Logs' }
]

// API Base URL
const API_BASE = 'http://localhost:5000/api'

// Message helper
const showMessage = (msg, type = 'success') => {
  message.value = msg
  messageType.value = type
  setTimeout(() => {
    message.value = ''
  }, 5000)
}

// Bulk operations
const toggleAllApplicants = () => {
  if (selectedApplicants.value.length === applicantsList.value.length) {
    selectedApplicants.value = []
  } else {
    selectedApplicants.value = applicantsList.value.map(a => a.Applicant_Id)
  }
}

const bulkDeleteApplicants = async () => {
  if (selectedApplicants.value.length === 0) return
  
  if (confirm(`Are you sure you want to delete ${selectedApplicants.value.length} applicants? This will also delete their exam attempts and login logs.`)) {
    try {
      await axios.post(`${API_BASE}/admin/applicants/bulk-delete`, {
        applicant_ids: selectedApplicants.value
      })
      await fetchApplicants()
      selectedApplicants.value = []
      showMessage(`Successfully deleted ${selectedApplicants.value.length} applicants`)
    } catch (error) {
      console.error('Error in bulk delete:', error)
      showMessage(error.response?.data?.error || 'Error deleting applicants', 'error')
    }
  }
}

const fetchAdmins = async () => {
  try {
    const response = await axios.get(`${API_BASE}/admin/admins`)
    adminsList.value = response.data
  } catch (error) {
    console.error('Error fetching admins:', error)
    showMessage('Error fetching admins data', 'error')
  }
}

const fetchLogs = async () => {
  try {
    const response = await axios.get(`${API_BASE}/admin/logs`)
    logsList.value = response.data
  } catch (error) {
    console.error('Error fetching logs:', error)
    showMessage('Error fetching logs data', 'error')
  }
}

// Admin methods
const addAdmin = async () => {
  try {
    await axios.post(`${API_BASE}/admin/admins`, adminForm.value)
    await fetchAdmins()
    closeAdminModal()
    showMessage('Admin added successfully')
  } catch (error) {
    console.error('Error adding admin:', error)
    showMessage(error.response?.data?.error || 'Error adding admin', 'error')
  }
}

const editAdmin = (admin) => {
  adminForm.value = { ...admin }
  showEditAdminModal.value = true
}

const updateAdmin = async () => {
  try {
    await axios.put(`${API_BASE}/admin/admins/${adminForm.value.Admin_ID}`, adminForm.value)
    await fetchAdmins()
    closeAdminModal()
    showMessage('Admin updated successfully')
  } catch (error) {
    console.error('Error updating admin:', error)
    showMessage(error.response?.data?.error || 'Error updating admin', 'error')
  }
}

const deleteAdmin = async (id) => {
  if (confirm('Are you sure you want to delete this admin?')) {
    try {
      await axios.delete(`${API_BASE}/admin/admins/${id}`)
      await fetchAdmins()
      showMessage('Admin deleted successfully')
    } catch (error) {
      console.error('Error deleting admin:', error)
      showMessage(error.response?.data?.error || 'Error deleting admin', 'error')
    }
  }
}

// Log methods
const viewLog = (log) => {
  selectedLog.value = log
  showViewLogModal.value = true
}

const deleteLog = async (id) => {
  if (confirm('Are you sure you want to delete this log entry?')) {
    try {
      await axios.delete(`${API_BASE}/admin/logs/${id}`)
      await fetchLogs()
      showMessage('Log deleted successfully')
    } catch (error) {
      console.error('Error deleting log:', error)
      showMessage(error.response?.data?.error || 'Error deleting log', 'error')
    }
  }
}

// Modal close methods
const closeAdminModal = () => {
  showAddAdminModal.value = false
  showEditAdminModal.value = false
  adminForm.value = {
    Admin_ID: null,
    Name: '',
    Email: '',
    Password: ''
  }
}

// Methods
const fetchFaculty = async () => {
  try {
    const response = await axios.get(`${API_BASE}/admin/faculty`)
    facultyList.value = response.data
  } catch (error) {
    console.error('Error fetching faculty:', error)
    showMessage('Error fetching faculty data', 'error')
  }
}

const fetchSchools = async () => {
  try {
    const response = await axios.get(`${API_BASE}/admin/schools`)
    schoolsList.value = response.data
  } catch (error) {
    console.error('Error fetching schools:', error)
    showMessage('Error fetching schools data', 'error')
  }
}

const fetchApplicants = async () => {
  try {
    const response = await axios.get(`${API_BASE}/admin/applicants`)
    applicantsList.value = response.data
  } catch (error) {
    console.error('Error fetching applicants:', error)
    showMessage('Error fetching applicants data', 'error')
  }
}

const addFaculty = async () => {
  try {
    await axios.post(`${API_BASE}/admin/faculty`, facultyForm.value)
    await fetchFaculty()
    closeFacultyModal()
    showMessage('Faculty added successfully')
  } catch (error) {
    console.error('Error adding faculty:', error)
    showMessage(error.response?.data?.error || 'Error adding faculty', 'error')
  }
}

const editFaculty = (faculty) => {
  facultyForm.value = { ...faculty }
  showEditFacultyModal.value = true
}

const updateFaculty = async () => {
  try {
    await axios.put(`${API_BASE}/admin/faculty/${facultyForm.value.Faculty_Id}`, facultyForm.value)
    await fetchFaculty()
    closeFacultyModal()
    showMessage('Faculty updated successfully')
  } catch (error) {
    console.error('Error updating faculty:', error)
    showMessage(error.response?.data?.error || 'Error updating faculty', 'error')
  }
}

const deleteFaculty = async (id) => {
  if (confirm('Are you sure you want to delete this faculty member?')) {
    try {
      await axios.delete(`${API_BASE}/admin/faculty/${id}`)
      await fetchFaculty()
      showMessage('Faculty deleted successfully')
    } catch (error) {
      console.error('Error deleting faculty:', error)
      showMessage(error.response?.data?.error || 'Error deleting faculty', 'error')
    }
  }
}

const addSchool = async () => {
  try {
    await axios.post(`${API_BASE}/admin/schools`, schoolForm.value)
    await fetchSchools()
    closeSchoolModal()
    showMessage('School added successfully')
  } catch (error) {
    console.error('Error adding school:', error)
    showMessage(error.response?.data?.error || 'Error adding school', 'error')
  }
}

const editSchool = (school) => {
  schoolForm.value = { ...school }
  showEditSchoolModal.value = true
}

const updateSchool = async () => {
  try {
    await axios.put(`${API_BASE}/admin/schools/${schoolForm.value.School_Id}`, schoolForm.value)
    await fetchSchools()
    closeSchoolModal()
    showMessage('School updated successfully')
  } catch (error) {
    console.error('Error updating school:', error)
    showMessage(error.response?.data?.error || 'Error updating school', 'error')
  }
}

const deleteSchool = async (id) => {
  if (confirm('Are you sure you want to delete this school?')) {
    try {
      await axios.delete(`${API_BASE}/admin/schools/${id}`)
      await fetchSchools()
      showMessage('School deleted successfully')
    } catch (error) {
      console.error('Error deleting school:', error)
      showMessage(error.response?.data?.error || 'Error deleting school', 'error')
    }
  }
}

const viewApplicant = (applicant) => {
  selectedApplicant.value = applicant
  showViewApplicantModal.value = true
}

const deleteApplicant = async (id) => {
  if (confirm('Are you sure you want to delete this applicant? This will also delete their exam attempts and login logs.')) {
    try {
      const response = await axios.delete(`${API_BASE}/admin/applicants/${id}`)
      await fetchApplicants()
      showMessage(response.data.message)
    } catch (error) {
      console.error('Error deleting applicant:', error)
      showMessage(error.response?.data?.error || 'Error deleting applicant', 'error')
    }
  }
}

const closeFacultyModal = () => {
  showAddFacultyModal.value = false
  showEditFacultyModal.value = false
  facultyForm.value = {
    Faculty_Id: null,
    F_Name: '',
    F_Email: '',
    School_Id: '',
    Designation: '',
    Password: ''
  }
}

const closeSchoolModal = () => {
  showAddSchoolModal.value = false
  showEditSchoolModal.value = false
  schoolForm.value = {
    School_Id: null,
    School_Name: '',
    School_Short: ''
  }
}

// Submit new applicant
const submitApplicant = async () => {
  try {
    const response = await axios.post(`${API_BASE}/applicants/add`, newApplicant.value)
    if (response.data.success) {
      showMessage('Applicant added successfully!')
      await fetchApplicants()
      showAddApplicantForm.value = false
      // Reset form
      newApplicant.value = {
        Full_Name: '',
        Email: '',
        Password: '',
        Phone: '',
        DOB: '',
        Gender: '',
        Address: ''
      }
    } else {
      showMessage(response.data.message || 'Failed to add applicant', 'error')
    }
  } catch (error) {
    console.error('Error adding applicant:', error)
    showMessage(error.response?.data?.error || 'Error adding applicant', 'error')
  }
}

// Handle file selection
const handleFileSelect = (event) => {
  selectedFile.value = event.target.files[0]
  uploadResults.value = null
  uploadProgress.value = 0
}

// Upload applicants from file
const uploadApplicants = async () => {
  if (!selectedFile.value) {
    showMessage('Please select a file first', 'error')
    return
  }

  const formData = new FormData()
  formData.append('file', selectedFile.value)

  try {
    isUploading.value = true
    uploadProgress.value = 0
    
    // Simulate progress
    const progressInterval = setInterval(() => {
      if (uploadProgress.value < 90) {
        uploadProgress.value += 10
      }
    }, 200)

    const response = await axios.post(`${API_BASE}/applicants/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    clearInterval(progressInterval)
    uploadProgress.value = 100

    if (response.data.success) {
      uploadResults.value = {
        success: response.data.successful_uploads || 0,
        errors: response.data.errors || []
      }
      await fetchApplicants()
      showMessage(`Successfully uploaded ${response.data.successful_uploads} applicants!`)
    } else {
      uploadResults.value = {
        success: 0,
        errors: [response.data.message || 'Upload failed']
      }
      showMessage('Upload failed', 'error')
    }
  } catch (error) {
    console.error('Error uploading applicants:', error)
    uploadResults.value = {
      success: 0,
      errors: [error.response?.data?.error || 'Upload failed']
    }
    showMessage('Error uploading applicants', 'error')
  } finally {
    isUploading.value = false
  }
}

// Close upload modal
const closeUploadModal = () => {
  showUploadApplicantsModal.value = false
  selectedFile.value = null
  uploadResults.value = null
  uploadProgress.value = 0
  isUploading.value = false
}

const getSchoolName = (schoolId) => {
  const school = schoolsList.value.find(s => s.School_Id === schoolId)
  return school ? school.School_Name : 'Unknown'
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString()
}

const logout = async () => {
  const email = localStorage.getItem('faculty_email') // Again, adjust if you use different keys for admin
  const role = 'Admin'
  
  try {
    // Call backend logout API
    await axios.post('http://localhost:5000/api/auth/logout', {
      email,
      role
    });
    
    // Clear local storage
    localStorage.removeItem('faculty_email')
    localStorage.removeItem('faculty_name')
    
    // Redirect to login page
    window.location.href = '/'
  } catch (err) {
    console.error('Logout error:', err);
    alert('Logout failed. Try again.');
  }
}

// Utility methods
const formatDateTime = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleString()
}

const getRoleColor = (role) => {
  switch (role) {
    case 'Admin': return 'bg-purple-100 text-purple-800'
    case 'Faculty': return 'bg-blue-100 text-blue-800'
    case 'Student': return 'bg-green-100 text-green-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

// Initialize
onMounted(async () => {
  const name = localStorage.getItem('faculty_name') // Reuse same key if you're not storing separately for admin
  if (name) adminName.value = name
  
  await fetchSchools()
  await fetchFaculty()
  await fetchApplicants()
  await fetchAdmins()
  await fetchLogs()
})
</script>
