<template>
  <div class="login-page">

    <!-- Left: Form -->
    <div class="form-side">
      <div class="form-card">

        <!-- Logo -->
        <div class="logo-wrap">
          <img
            src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTpCQrjNAF4Mn0LHjgvQizYtxEzhovvhVohzw&s"
            class="logo"
            alt="Navrachna University Logo"
          />
        </div>

        <h2 class="title">Examination Portal</h2>
        <p class="subtitle-accent">Management System</p>
        <p class="tagline">Secure. Smart. Seamless.</p>

        <div class="fields">
          <!-- Email -->
          <div class="field">
            <label>Email Address</label>
            <div class="input-wrap">
              <span class="input-icon">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
              </span>
              <input v-model="email" type="email" placeholder="Enter your email" />
            </div>
          </div>

          <!-- Password -->
          <div class="field">
            <label>Password</label>
            <div class="input-wrap">
              <span class="input-icon">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              </span>
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Enter your password"
              />
              <button class="toggle-pw" @click="showPassword = !showPassword" type="button" tabindex="-1">
                <svg v-if="!showPassword" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/></svg>
                <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
              </button>
            </div>
          </div>

          <!-- Error -->
          <p v-if="message" class="error-msg">{{ message }}</p>

          <!-- Login Button -->
          <button
            @click="login"
            :disabled="loading || !email || !password || !validateEmail(email)"
            class="login-btn"
          >
            <span v-if="!loading">Login</span>
            <span v-else class="loading-dots">
              <span></span><span></span><span></span>
            </span>
          </button>

          <p class="copyright">© 2026 Navrachna University. All rights reserved.</p>
        </div>
      </div>
    </div>

    <!-- Right: Illustration -->
    <div class="illustration-side">
      <div class="dots-grid"></div>
      <div class="hero-content">
        <h1 class="hero-title">One Platform. <br> Endless Possibilities.</h1>
        <h2 class="hero-title gradient-text">Empower Education for Everyone.</h2>
        <img :src="illustrationSrc" class="illustration" alt="Exam Illustration" />
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from '../utils/axiosInstance'

const illustrationSrc = '/exam-illustration.png'
const loading = ref(false)
const email = ref("")
const password = ref("")
const message = ref("")
const showPassword = ref(false)
const router = useRouter()
let messageTimer = null

onMounted(() => {
  const expired = localStorage.getItem("session_expired")
  if (expired) {
    showMessage("Session expired. You were automatically logged out.")
    localStorage.removeItem("session_expired")
  }
  const token = localStorage.getItem('token')
  if (token) {
    const role = localStorage.getItem('active_role')
    if (role) router.replace(`/${role.toLowerCase()}`)
  }
  history.replaceState(null, '', '/')
  history.pushState(null, '', '/')
})

const showMessage = (text, duration = 3500) => {
  message.value = text
  if (messageTimer) clearTimeout(messageTimer)
  messageTimer = setTimeout(() => { message.value = "" }, duration)
}

const validateEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)

const login = async () => {
  if (!email.value && !password.value) return showMessage("Email and Password cannot be empty")
  if (!email.value) return showMessage("Email cannot be empty")
  if (!validateEmail(email.value)) return showMessage("Please enter a valid email address")
  if (!password.value) return showMessage("Password cannot be empty")

  loading.value = true
  try {
    const response = await axios.post('/auth/login', { email: email.value, password: password.value })
    const res = response.data
    if (res.status !== "success") {
      showMessage(res.message || "Invalid credentials")
      loading.value = false
      return
    }
    localStorage.setItem("token", res.token)
    localStorage.setItem("roles", JSON.stringify(res.roles))
    localStorage.setItem("active_role", res.active_role)
    localStorage.setItem("email", res.email)
    localStorage.setItem("name", res.name)
    localStorage.setItem("login_time", Date.now())
    if (res.applicant_id) localStorage.setItem("applicant_id", res.applicant_id)
    if (res.faculty_id) localStorage.setItem("faculty_id", res.faculty_id)
    if (res.admin_id) localStorage.setItem("admin_id", res.admin_id)
    setTimeout(() => router.replace(`/${res.active_role.toLowerCase()}`), 50)
  } catch (e) {
    showMessage(e.response?.data?.message || "Unable to login. Please try again.")
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Sora:wght@600;700;800&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

/* ── Full page: single gradient bg across both sides ── */
.login-page {
  min-height: 100vh;
  display: flex;
  font-family: 'DM Sans', sans-serif;
  background: linear-gradient(135deg, #e8e0ff 0%, #f0d6f5 30%, #fce4f0 60%, #ddd6fe 100%);
}

/* ── LEFT: transparent, just centers the white card ── */
.form-side {
  width: 45%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 40px;
}

/* ── WHITE CARD ── */
.form-card {
  width: 100%;
  max-width: 400px;
  background: #ffffff;
  border-radius: 24px;
  padding: 40px 36px;
  box-shadow:
    0 4px 6px rgba(0, 0, 0, 0.04),
    0 20px 60px rgba(108, 99, 255, 0.18);
  animation: slideUp 0.5s cubic-bezier(0.22, 1, 0.36, 1) both;
}

/* ── Logo ── */
.logo-wrap {
  display: flex;
  justify-content: center;
  margin-bottom: 18px;
}

.logo {
  height: 72px;
  object-fit: contain;
}

/* ── Titles ── */
.title {
  font-family: 'Sora', sans-serif;
  font-size: 1.45rem;
  font-weight: 700;
  color: #1a1a2e;
  text-align: center;
}

.subtitle-accent {
  font-family: 'Sora', sans-serif;
  font-size: 1rem;
  font-weight: 600;
  text-align: center;
  background: linear-gradient(90deg, #6c63ff, #c86dd7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-top: 2px;
}

.tagline {
  text-align: center;
  font-size: 0.78rem;
  color: #9ca3af;
  letter-spacing: 0.05em;
  margin-top: 6px;
  margin-bottom: 28px;
}

/* ── Fields ── */
.fields { display: flex; flex-direction: column; gap: 16px; }

.field { display: flex; flex-direction: column; gap: 6px; }

.field label {
  font-size: 0.82rem;
  font-weight: 600;
  color: #374151;
}

.input-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 13px;
  color: #9ca3af;
  display: flex;
  align-items: center;
  pointer-events: none;
}

.input-wrap input {
  width: 100%;
  padding: 11px 14px 11px 40px;
  border: 1.5px solid #e5e7eb;
  border-radius: 10px;
  font-size: 0.9rem;
  font-family: 'DM Sans', sans-serif;
  color: #1a1a2e;
  background: #f9fafb;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s, background 0.2s;
}

.input-wrap input::placeholder { color: #c4c9d4; }

.input-wrap input:focus {
  border-color: #6c63ff;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(108, 99, 255, 0.1);
}

.toggle-pw {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  cursor: pointer;
  color: #9ca3af;
  display: flex;
  align-items: center;
  padding: 2px;
  transition: color 0.2s;
}
.toggle-pw:hover { color: #6c63ff; }

/* ── Error ── */
.error-msg {
  font-size: 0.82rem;
  color: #ef4444;
  text-align: center;
  font-weight: 500;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  padding: 8px 12px;
}

/* ── Login Button ── */
.login-btn {
  width: 100%;
  padding: 13px;
  background: linear-gradient(135deg, #6c63ff 0%, #c86dd7 100%);
  color: #fff;
  font-size: 0.95rem;
  font-weight: 600;
  font-family: 'DM Sans', sans-serif;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 4px 18px rgba(108, 99, 255, 0.4);
  margin-top: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 46px;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(108, 99, 255, 0.5);
}

.login-btn:disabled {
  background: #e5e7eb;
  color: #9ca3af;
  cursor: not-allowed;
  box-shadow: none;
}

.loading-dots { display: flex; gap: 5px; align-items: center; }
.loading-dots span {
  width: 6px; height: 6px;
  background: rgba(255,255,255,0.85);
  border-radius: 50%;
  animation: bounce 0.8s ease-in-out infinite;
}
.loading-dots span:nth-child(2) { animation-delay: 0.15s; }
.loading-dots span:nth-child(3) { animation-delay: 0.3s; }

@keyframes bounce {
  0%, 80%, 100% { transform: translateY(0); opacity: 0.6; }
  40%            { transform: translateY(-6px); opacity: 1; }
}

.copyright {
  text-align: center;
  font-size: 0.75rem;
  color: #c4c9d4;
  margin-top: 8px;
}

/* ── RIGHT: no separate background, blends into page gradient ── */
.illustration-side {
  width: 55%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.dots-grid {
  position: absolute;
  top: 50px;
  right: 60px;
  width: 130px;
  height: 130px;
  background-image: radial-gradient(circle, rgba(108,99,255,0.3) 1.5px, transparent 1.5px);
  background-size: 14px 14px;
  opacity: 0.5;
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 520px;
  padding: 40px;
  animation: fadeInRight 0.6s cubic-bezier(0.22, 1, 0.36, 1) 0.1s both;
}

.hero-title {
  font-family: 'Sora', sans-serif;
  font-size: 2.4rem;
  font-weight: 800;
  color: #1a1a2e;
  line-height: 1.2;
}

.gradient-text {
  background: linear-gradient(90deg, #6c63ff 0%, #c86dd7 55%, #f472b6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.illustration {
  width: 100%;
  max-width: 500px;
  margin-top: 28px;
  filter: drop-shadow(0 20px 40px rgba(108, 99, 255, 0.15));
  animation: float 4s ease-in-out infinite;
}

/* ── Animations ── */
@keyframes slideUp {
  from { opacity: 0; transform: translateY(28px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInRight {
  from { opacity: 0; transform: translateX(30px); }
  to   { opacity: 1; transform: translateX(0); }
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50%       { transform: translateY(-10px); }
}

/* ── Responsive ── */
@media (max-width: 900px) {
  .login-page { flex-direction: column; }
  .form-side  { width: 100%; padding: 40px 24px; }
  .illustration-side { width: 100%; padding: 32px 24px 40px; }
  .hero-title { font-size: 1.8rem; }
}
</style>