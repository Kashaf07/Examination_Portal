import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Admin from '../views/Admin.vue'
import Faculty from '../views/Faculty.vue'
import Student from '../views/Student.vue'
import CreateExamForm from '../components/CreateExamForm.vue'


import AddStudentsPage from '../views/AddStudentsPage.vue'
import AddQuestionBankPage from '../views/AddQuestionBankPage.vue'
import MakeQuestionPaperPage from '../views/MakeQuestionPaperPage.vue'

const routes = [
  { path: '/', component: Login },
  { path: '/admin', component: Admin },
  { path: '/faculty', component: Faculty },
  { path: '/student', component: Student },
  { path: '/create-exam', component: CreateExamForm },
   {
    path: '/exam/:examId/add-students',
    name: 'AddStudents',
    component: AddStudentsPage,
  },
  {
    path: '/exam/:examId/add-question-bank',
    name: 'AddQuestionBank',
    component: AddQuestionBankPage,
  },
  {
    path: '/exam/:examId/make-question-paper',
    name: 'MakeQuestionPaper',
    component: MakeQuestionPaperPage,
  },
  
]

export default createRouter({
  history: createWebHistory(),
  routes
})

