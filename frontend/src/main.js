import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'
import './assets/main.css'

createApp(App).use(router).mount('#app')

// Prevent bfcache restoring stale authenticated pages
window.addEventListener('pageshow', (event) => {
  if (event.persisted) {
    window.location.reload()
  }
})

window.addEventListener('popstate', () => {
  const token = localStorage.getItem('token')
  const currentPath = window.location.pathname

  // Only intercept if logged in AND the browser tried to go to login (/) or outside app
  if (token && (currentPath === '/' || currentPath === '')) {
    // Push forward again — cancel the navigation
    history.pushState(null, '', window.location.href)

    const confirmed = window.confirm('Do you want to logout?')
    if (confirmed) {
      localStorage.clear()
      window.location.replace('/')
    } else {
      // Stay where they are — push them back to their protected route
      const role = localStorage.getItem('active_role') || 'admin'
      history.pushState(null, '', `/${role.toLowerCase()}`)
    }
  }
})