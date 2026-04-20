<template>
  <div class="login-page">

    <!-- Left: Form (50%) -->
    <div class="form-side">
      <div class="form-card">
        <div class="logo-wrap">
          <img
            src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTpCQrjNAF4Mn0LHjgvQizYtxEzhovvhVohzw&s"
            class="logo"
            alt="Navrachna University Logo"
          />
        </div>

        <h2 class="title">Examination Portal</h2>
        <p class="subtitle">Login with your credentials</p>

        <div class="fields">
          <div class="field">
            <label>Email</label>
            <input v-model="email" type="email" placeholder="Enter Email" />
          </div>

          <div class="field">
            <label>Password</label>
            <input v-model="password" type="password" placeholder="Enter Password" />
          </div>

          <p v-if="message" class="error-msg">{{ message }}</p>

          <button
            @click="login"
            :disabled="loading || !email || !password || !validateEmail(email)"
            class="login-btn"
          >
            {{ loading ? "Please wait..." : "Login" }}
          </button>
        </div>
      </div>
    </div>

    <!-- Right: Video (50%) -->
    <div class="video-side">
      <video class="hero-video" :src="videoSrc" autoplay loop muted playsinline></video>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from '../utils/axiosInstance'

const loading = ref(false)
const email = ref("")
const password = ref("")
const message = ref("")
const router = useRouter()
const videoSrc = '/login.mp4'
let messageTimer = null

onMounted(() => {
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
/* ── Page ── */
.login-page {
  min-height: 100vh;
  display: flex;
  background: #eef2ff;
  overflow: hidden;
}

/* ── Left: Form side (50%) ── */
.form-side {
  width: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 40px;
  background: #eef2ff;
}

/* ── Form card ── */
.form-card {
  width: 100%;
  max-width: 420px;
  background: #ffffff;
  border-radius: 24px;
  padding: 48px 44px;
  box-shadow:
    0 0 0 1px rgba(99, 102, 241, 0.08),
    0 4px 24px rgba(99, 102, 241, 0.18),
    0 0 60px rgba(99, 102, 241, 0.12),
    0 0 120px rgba(139, 92, 246, 0.08);
  animation: cardIn 0.55s cubic-bezier(0.34, 1.56, 0.64, 1) both;
  transition: box-shadow 0.3s ease;
}

.form-card:hover {
  box-shadow:
    0 0 0 1px rgba(99, 102, 241, 0.12),
    0 8px 32px rgba(99, 102, 241, 0.28),
    0 0 80px rgba(99, 102, 241, 0.18),
    0 0 160px rgba(139, 92, 246, 0.12);
}

/* ── Logo ── */
.logo-wrap {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.logo {
  height: 90px;
  object-fit: contain;
  filter: drop-shadow(0 2px 8px rgba(99, 102, 241, 0.2));
}

/* ── Headings ── */
.title {
  font-size: 1.75rem;
  font-weight: 700;
  text-align: center;
  color: #1e1b4b;
  margin-bottom: 6px;
}

.subtitle {
  text-align: center;
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 28px;
}

/* ── Fields ── */
.fields {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #374151;
}

.field input {
  padding: 10px 14px;
  border: 1.5px solid #e5e7eb;
  border-radius: 10px;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
  background: #fafafa;
  color: #111827;
}

.field input:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
  background: #fff;
}

/* ── Error ── */
.error-msg {
  font-size: 0.85rem;
  color: #dc2626;
  text-align: center;
  font-weight: 500;
}

/* ── Button ── */
.login-btn {
  width: 100%;
  padding: 11px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.15s, box-shadow 0.2s;
  box-shadow: 0 4px 18px rgba(99, 102, 241, 0.35);
}

.login-btn:hover:not(:disabled) {
  opacity: 0.92;
  transform: translateY(-1px);
  box-shadow: 0 6px 24px rgba(99, 102, 241, 0.45);
}

.login-btn:disabled {
  background: linear-gradient(135deg, #a5b4fc, #c4b5fd);
  cursor: not-allowed;
  box-shadow: none;
}

/* ── Right: Video side (50%) ── */
.video-side {
  width: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px 32px;
  background: #eef2ff;
}

.hero-video {
  width: 100%;
  max-width: 640px;
  height: 520px;
  object-fit: cover;
  border-radius: 20px;
  background: #eef2ff;
  filter: drop-shadow(0 12px 36px rgba(99, 102, 241, 0.2));
}

/* ── Animation ── */
@keyframes cardIn {
  0%   { opacity: 0; transform: scale(0.75); }
  65%  { opacity: 1; transform: scale(1.04); }
  82%  { transform: scale(0.97); }
  100% { transform: scale(1); }
}

/* ── Responsive ── */
@media (max-width: 768px) {
  .login-page  { flex-direction: column; }
  .form-side   { width: 100%; padding: 32px 20px; }
  .video-side  { width: 100%; padding: 0 20px 32px; }
  .hero-video  { max-height: 45vh; }
}
</style>
