import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Admin from '../views/Admin.vue'
import Faculty from '../views/Faculty.vue'
import Student from '../views/Student.vue'
import AddQuestion from '../components/AddQuestion.vue'
import UploadQuestionBank from '../views/UploadQuestionBank.vue'
import CreateExamForm from '../components/CreateExamForm.vue'
import MakeQuestionPaperPage from '../views/MakeQuestionPaperPage.vue'
import UploadStudents from '../views/UploadStudents.vue'
import AddApplicantsPage from '../views/AddApplicantsPage.vue'
import AddApplicants_exam from '../views/AddApplicants_exam.vue'
import ViewResponsesAdmin from '../views/ViewResponsesAdmin.vue'
import ViewResponsesFaculty from '../views/ViewResponses.vue'
import ViewAnswers from '../views/ViewAnswers.vue'


// ✅ Define routes
const routes = [
  { path: '/', component: Login, name: 'Login' },
  { path: "/admin", component: Admin, name: "Admin", meta: { requiresAuth: true, role: "Admin" }, redirect: "/admin/faculty",
  children: [
    { path: "faculty", name: "AdminFaculty", component: () => import("../views/admin/AdminFaculty.vue"),},
    { path: "schools", name: "AdminSchools", component: () => import("../views/admin/AdminSchools.vue"),},
    { path: "designations", name: "AdminDesignations", component: () => import("../views/admin/DesignationManagement.vue") },
    { path: "applicants", name: "AdminApplicants", component: () => import("../views/admin/AdminApplicants.vue"),},
    { path: "exams", name: "AdminExams", component: () => import("../views/admin/AdminExams.vue"),},
    { path: "admins", name: "AdminAdmins", component: () => import("../views/admin/AdminAdmins.vue"),},
    { path: "logs", name: "AdminLogs", component: () => import("../views/admin/AdminLogs.vue"),},
    { path: "upload-students", name: "AdminUploadStudents", component: () => import("../views/UploadStudents.vue"), meta: { requiresAuth: true, role: "Admin" }}
  ]},

  { path: '/faculty', name: 'Faculty', component: Faculty, meta: { requiresAuth: true, role: 'Faculty' } },
  { path: '/student', name: 'Student', component: Student, meta: { requiresAuth: true, role: 'Student' } },
  

  // Admin + Faculty shared routes
  { path: '/exam/:examId/upload-question-bank', name: 'UploadQuestionBank', component: UploadQuestionBank, meta: { requiresAuth: true, role: ['Admin', 'Faculty'] } },
  { path: '/create-exam', component: CreateExamForm, meta: { requiresAuth: true, role: ['Admin', 'Faculty'] } },
  { path: '/upload-students', name: 'UploadStudents', component: UploadStudents, meta: { requiresAuth: true, role: ['Admin', 'Faculty'] } },
  { path: '/exam/:examId/add-applicants-exam', name: 'AddApplicantsexam', component: AddApplicants_exam, meta: { requiresAuth: true, role: ['Admin', 'Faculty'] } },
  { path: '/exam/:examId/add-question', name: 'AddQuestion', component: AddQuestion, meta: { requiresAuth: true, role: ['Admin', 'Faculty'] } },
  { path: '/exam/:examId/make-question-paper', name: 'MakeQuestionPaper', component: MakeQuestionPaperPage, meta: { requiresAuth: true, role: ['Admin', 'Faculty'] } },
  { path: '/add-applicants', name: 'AddApplicants', component: AddApplicantsPage, meta: { requiresAuth: true, role: ['Admin', 'Faculty'] } },
  { path: '/view-answers/:attemptId', name: 'ViewAnswers', component: ViewAnswers, props: true, meta: { requiresAuth: true, role: ['Admin', 'Faculty'] } },

  // Admin specific
  { path: '/responses/:examId', name: 'ViewResponsesAdmin', component: ViewResponsesAdmin, props: true, meta: { requiresAuth: true, role: 'Admin' } },

  // Faculty specific
  { path: '/faculty/view-responses/:examId', name: 'ViewResponses', component: ViewResponsesFaculty, props: true, meta: { requiresAuth: true, role: 'Faculty' } },
  {
  path: '/groups',
  name: 'Groups',
  component: () => import('../views/Groups.vue')
},
{ path: '/:pathMatch(.*)*', redirect: '/' }
]

// ✅ Create router
const router = createRouter({
  history: createWebHistory(),
  routes
})

// ✅ Enhanced Navigation Guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token")
  const activeRole = localStorage.getItem("active_role") // NEW SYSTEM
  const roles = JSON.parse(localStorage.getItem("roles") || "[]")

  // Get required role for route
  const routeMeta = to.matched.find(record => record.meta && record.meta.role)
  const requiredRole = routeMeta ? routeMeta.meta.role : null

  console.log(
    `🔒 Navigating to: ${to.path} | Required: ${requiredRole} | Active: ${activeRole} | Roles: ${roles}`
  )

  // --- PUBLIC ROUTE (login) ---
  if (!requiredRole) {
    return next()
  }

  // --- AUTH REQUIRED ---
  if (!token || !activeRole) {
    return next("/")
  }

  // Convert requiredRole to array for easy checking
  const requiredList = Array.isArray(requiredRole)
    ? requiredRole.map(r => r.toLowerCase())
    : [requiredRole.toLowerCase()]

  // Check if user's roles include ANY required role
  const hasRequiredRole = roles
    .map(r => r.toLowerCase())
    .some(r => requiredList.includes(r))

  if (!hasRequiredRole) {
    alert("Access denied!")
    return next(`/${activeRole.toLowerCase()}`)
  }

  // All good
  return next()
})


export default router
