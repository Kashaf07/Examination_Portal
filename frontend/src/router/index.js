import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Admin from '../views/Admin.vue'
import Faculty from '../views/Faculty.vue'
import Student from '../views/Student.vue'

const routes = [
  { path: '/', component: Login },
  { path: '/admin', component: Admin },
  { path: '/faculty', component: Faculty },
  { path: '/student', component: Student },
]

export default createRouter({
  history: createWebHistory(),
  routes
})
