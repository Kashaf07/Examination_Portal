import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Admin from '../views/Admin.vue'
import Faculty from '../views/Faculty.vue'
import Student from '../views/Student.vue'
import AddQuestion from '../components/AddQuestion.vue'
import UploadQuestionBank from '../views/UploadQuestionBank.vue';
import CreateExamForm from '../components/CreateExamForm.vue'
import AddStudentsPage from '../views/AddStudentsPage.vue'
import MakeQuestionPaperPage from '../views/MakeQuestionPaperPage.vue'
import AddApplicantsPage from '../views/AddApplicantsPage.vue'


const routes = [
  { path: '/', component: Login },
  { path: '/admin', component: Admin },
  { path: '/faculty', component: Faculty },
  { path: '/student', component: Student },
  { path: '/exam/:examId/upload-question-bank', name: 'UploadQuestionBank', component: UploadQuestionBank },
  { path: '/create-exam', component: CreateExamForm },
  { path: '/exam/:examId/add-students', name: 'AddStudents', component: AddStudentsPage },
  { path: '/exam/:examId/add-question', name: 'AddQuestion', component: AddQuestion },
  { path: '/exam/:examId/make-question-paper', name: 'MakeQuestionPaper', component: MakeQuestionPaperPage },
  {path: '/add-applicants',name: 'AddApplicants',component: AddApplicantsPage}
]

export default createRouter({
  history: createWebHistory(),
  routes
})

