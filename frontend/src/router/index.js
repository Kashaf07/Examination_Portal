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

const routes = [
  { path: '/', component: Login },
  { path: '/admin', component: Admin },
  { path: '/faculty', component: Faculty },
  { path: '/student', component: Student },
  { path: '/exam/:examId/upload-question-bank', name: 'UploadQuestionBank', component: UploadQuestionBank },
  { path: '/create-exam', component: CreateExamForm },
  { path: '/upload-students', name:'UploadStudents', component: UploadStudents },
  { path: '/exam/:examId/add-applicants-exam', name: 'AddApplicantsexam', component: AddApplicants_exam },
  { path: '/exam/:examId/add-question', name: 'AddQuestion', component: AddQuestion },
  { path: '/exam/:examId/make-question-paper', name: 'MakeQuestionPaper', component: MakeQuestionPaperPage },
  { path: '/add-applicants', name: 'AddApplicants', component: AddApplicantsPage },
  {
    path: '/faculty/view-responses/:examId',
    name: 'ViewResponses',
    component: () => import('@/views/ViewResponses.vue'),
    props: true
  },
  {
    path: '/faculty/view-answers/:attemptId',
    name: 'ViewAnswers',
    component: () => import('@/views/ViewAnswers.vue'),
    props: true
  },
  {
  path: '/faculty',
  name: 'Faculty',
  component: () => import('@/views/Faculty.vue')
  
}

  
]

export default createRouter({
  history: createWebHistory(),
  routes
})
