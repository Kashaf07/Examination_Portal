import { createRouter, createWebHistory } from 'vue-router'

// Core views
import Login from '../views/Login.vue'
import Admin from '../views/Admin.vue'
import Faculty from '../views/Faculty.vue'
import Student from '../views/Student.vue'

// Shared / feature views
import AddQuestion from '../components/AddQuestion.vue'
import UploadQuestionBank from '../views/UploadQuestionBank.vue'
import MakeQuestionPaperPage from '../views/MakeQuestionPaperPage.vue'
import UploadStudents from '../views/UploadStudents.vue'
import AddApplicantsPage from '../views/AddApplicantsPage.vue'
import AddApplicants_exam from '../views/AddApplicants_exam.vue'
import ViewResponsesAdmin from '../views/ViewResponsesAdmin.vue'
import ViewResponsesFaculty from '../views/ViewResponses.vue'
import ViewAnswers from '../views/ViewAnswers.vue'

// ---------------- ROUTES ----------------
const routes = [
  { path: '/', component: Login, name: 'Login' },

  {
    path: '/admin',
    component: Admin,
    name: 'Admin',
    meta: { requiresAuth: true, role: 'Admin' },
    redirect: '/admin/faculty',
    children: [
      { path: 'faculty', name: 'AdminFaculty', component: () => import('../views/admin/AdminFaculty.vue') },
      { path: 'schools', name: 'AdminSchools', component: () => import('../views/admin/AdminSchools.vue') },
      { path: 'designations', name: 'AdminDesignations', component: () => import('../views/admin/DesignationManagement.vue') },
      { path: 'role-assignment', name: 'AdminRoleAssignment', component: () => import('../views/admin/AdminRoleAssignment.vue') },
      { path: 'groups', name: 'AdminApplicantGroups', component: () => import('../views/Groups.vue') },
      { path: 'applicants', name: 'AdminApplicants', component: () => import('../views/admin/AdminApplicants.vue') },

      /* ================= FACULTY GROUPS (ADMIN) ================= */

      {
        path: 'faculty-groups',
        name: 'AdminFacultyGroups',
        component: () => import('@/views/Groups.vue')
      },
      {
        path: 'faculty-groups/add',
        name: 'AdminAddFacultyGroup',
        component: () => import('@/views/AddFacultyGroup.vue')
      },
      {
        path: 'faculty-groups/:groupId/add-faculty',
        name: 'AdminAddFacultyToGroup',
        component: () => import('@/views/AddFaculty.vue'),
        props: true
      },

      /* =========================================================== */

      { path: 'applicants/add', name: 'AddApplicant', component: () => import('@/views/AddApplicantsPage.vue') },
      { path: 'exams', name: 'AdminExams', component: () => import('../views/admin/AdminExams.vue') },
      { path: 'admins', name: 'AdminAdmins', component: () => import('../views/admin/AdminAdmins.vue') },
      { path: 'logs', name: 'AdminLogs', component: () => import('../views/admin/AdminLogs.vue') },
      {
        path: 'upload-students',
        name: 'AdminUploadStudents',
        component: UploadStudents,
        meta: { requiresAuth: true, role: 'Admin' }
      }
    ]
  },

  // ---------------- FACULTY ----------------
  {
    path: '/faculty',
    name: 'Faculty',
    component: Faculty,
    meta: { requiresAuth: true, role: 'Faculty' }
  },
  {
    path: '/faculty/groups',
    name: 'FacultyApplicantGroups',
    component: () => import('../views/Groups.vue'),
    meta: { requiresAuth: true, role: 'Faculty' }
  },

  // ---------------- STUDENT ----------------
  {
    path: '/student',
    name: 'Student',
    component: Student,
    meta: { requiresAuth: true, role: 'Student' }
  },

  // ---------------- SHARED (ADMIN + FACULTY) ----------------
  {
    path: '/exam/:examId/upload-question-bank',
    name: 'UploadQuestionBank',
    component: UploadQuestionBank,
    meta: { requiresAuth: true, role: ['Admin', 'Faculty'] }
  },
  {
    path: '/upload-students',
    name: 'UploadStudents',
    component: UploadStudents,
    meta: { requiresAuth: true, role: ['Admin', 'Faculty'] }
  },
  {
    path: '/exam/:examId/add-applicants-exam',
    name: 'AddApplicantsExam',
    component: AddApplicants_exam,
    meta: { requiresAuth: true, role: ['Admin', 'Faculty'] }
  },
  {
    path: '/exam/:examId/add-question',
    name: 'AddQuestion',
    component: AddQuestion,
    meta: { requiresAuth: true, role: ['Admin', 'Faculty'] }
  },
  {
    path: '/exam/:examId/make-question-paper',
    name: 'MakeQuestionPaper',
    component: MakeQuestionPaperPage,
    meta: { requiresAuth: true, role: ['Admin', 'Faculty'] }
  },
  {
    path: '/add-applicants',
    name: 'AddApplicants',
    component: AddApplicantsPage,
    meta: { requiresAuth: true, role: ['Admin', 'Faculty'] }
  },
  {
    path: '/view-answers/:attemptId',
    name: 'ViewAnswers',
    component: ViewAnswers,
    props: true,
    meta: { requiresAuth: true, role: ['Admin', 'Faculty'] }
  },

  // ---------------- RESPONSES ----------------
  {
    path: '/responses/:examId',
    name: 'ViewResponsesAdmin',
    component: ViewResponsesAdmin,
    props: true,
    meta: { requiresAuth: true, role: 'Admin' }
  },
  {
    path: '/faculty/view-responses/:examId',
    name: 'ViewResponsesFaculty',
    component: ViewResponsesFaculty,
    props: true,
    meta: { requiresAuth: true, role: 'Faculty' }
  },

  // ---------------- FALLBACK ----------------
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

// ---------------- ROUTER ----------------
const router = createRouter({
  history: createWebHistory(),
  routes
})

// ---------------- AUTH GUARD ----------------
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const activeRole = localStorage.getItem('active_role')
  const roles = JSON.parse(localStorage.getItem('roles') || '[]')

  const routeMeta = to.matched.find(r => r.meta && r.meta.role)
  const requiredRole = routeMeta ? routeMeta.meta.role : null

  if (!requiredRole) return next()
  if (!token || !activeRole) return next('/')

  const requiredRoles = Array.isArray(requiredRole)
    ? requiredRole.map(r => r.toLowerCase())
    : [requiredRole.toLowerCase()]

  const hasAccess = roles.map(r => r.toLowerCase()).some(r => requiredRoles.includes(r))

  if (!hasAccess) {
    alert('Access denied!')
    return next(`/${activeRole.toLowerCase()}`)
  }

  next()
})

export default router
