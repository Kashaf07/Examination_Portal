<template>
  <div class="login-page">

    <!-- Left: Form (50%) -->
    <div class="form-side">
      <div class="form-card">
        <div class="fog-blob"></div>
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
  const expired = localStorage.getItem("session_expired");

  if (expired) {
    showMessage("Session expired. You were automatically logged out.");
    localStorage.removeItem("session_expired");
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
/* ── Page ── */
.login-page {
  min-height: 100vh;
  display: flex;
  background: #ffffff;
  overflow: hidden;
}

/* ── Left: Form side (50%) ── */
.form-side {
  width: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 40px;
  background: #ffffff;
}

/* ── Form card ── */
.form-card {
  width: 100%;
  max-width: 420px;
  background: #4d5f8e;
  border-radius: 24px;
  padding: 48px 44px;
  position: relative;
  overflow: hidden;
  box-shadow:
    0 0 0 1px rgba(255, 255, 255, 0.08),
    0 8px 40px rgba(20, 30, 70, 0.45);
  animation: cardIn 0.55s cubic-bezier(0.34, 1.56, 0.64, 1) both;
  transition: box-shadow 0.3s ease;
}

.form-card:hover {
  box-shadow:
    0 0 0 1px rgba(255, 255, 255, 0.12),
    0 12px 50px rgba(20, 30, 70, 0.55);
}

/* ── Smoky fog blobs ── */
.form-card::before,
.form-card::after {
  content: '';
  position: absolute;
  border-radius: 50%;
  filter: blur(55px);
  opacity: 0.45;
  pointer-events: none;
  z-index: 0;
}

.form-card::before {
  width: 280px;
  height: 280px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.18) 0%, rgba(255, 255, 255, 0.06) 50%, transparent 70%);
  top: -80px;
  left: -80px;
  animation: fogDrift1 8s ease-in-out infinite alternate;
}

.form-card::after {
  width: 260px;
  height: 260px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.14) 0%, rgba(255, 255, 255, 0.05) 50%, transparent 70%);
  bottom: -70px;
  right: -70px;
  animation: fogDrift2 10s ease-in-out infinite alternate;
}

/* extra fog blob via wrapper */
.fog-blob {
  position: absolute;
  width: 220px;
  height: 220px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.04) 50%, transparent 70%);
  filter: blur(50px);
  opacity: 0.6;
  bottom: 20px;
  left: -60px;
  pointer-events: none;
  z-index: 0;
  animation: fogDrift3 12s ease-in-out infinite alternate;
}

/* ensure form content sits above fog */
.logo-wrap, .title, .subtitle, .fields {
  position: relative;
  z-index: 1;
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
  filter: drop-shadow(0 2px 10px rgba(0, 0, 0, 0.3)) brightness(1.05);
}

/* ── Headings ── */
.title {
  font-size: 1.75rem;
  font-weight: 700;
  text-align: center;
  color: #ffffff;
  margin-bottom: 6px;
}

.subtitle {
  text-align: center;
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.6);
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
  color: rgba(255, 255, 255, 0.85);
}

.field input {
  padding: 10px 14px;
  border: 1.5px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s, background 0.2s;
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.field input::placeholder {
  color: rgba(255, 255, 255, 0.35);
}

.field input:focus {
  border-color: rgba(255, 255, 255, 0.5);
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.14);
}

/* ── Error ── */
.error-msg {
  font-size: 0.85rem;
  color: #fca5a5;
  text-align: center;
  font-weight: 500;
}

/* ── Button ── */
.login-btn {
  width: 100%;
  padding: 12px;
  background: #ffffff;
  color: #4d5f8e;
  font-size: 1rem;
  font-weight: 700;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  letter-spacing: 0.03em;
  transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
  box-shadow: 0 4px 18px rgba(255, 255, 255, 0.3);
}

.login-btn:hover:not(:disabled) {
  background: #f0f4ff;
  transform: translateY(-1px);
  box-shadow: 0 6px 24px rgba(255, 255, 255, 0.45);
}

.login-btn:disabled {
  background: rgba(255, 255, 255, 0.25);
  cursor: not-allowed;
  box-shadow: none;
  color: rgba(44, 62, 107, 0.4);
}

/* ── Right: Video side (50%) ── */
.video-side {
  width: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: #ffffff;
}

.hero-video {
  width: 100%;
  height: 90vh;
  object-fit: cover;
  border-radius: 0;
  display: block;
}

/* ── Animation ── */
@keyframes cardIn {
  0%   { opacity: 0; transform: scale(0.75); }
  65%  { opacity: 1; transform: scale(1.04); }
  82%  { transform: scale(0.97); }
  100% { transform: scale(1); }
}

@keyframes fogDrift1 {
  0%   { transform: translate(0px, 0px) scale(1); opacity: 0.45; }
  33%  { transform: translate(40px, 30px) scale(1.1); opacity: 0.55; }
  66%  { transform: translate(20px, 60px) scale(0.95); opacity: 0.38; }
  100% { transform: translate(60px, 20px) scale(1.05); opacity: 0.5; }
}

@keyframes fogDrift2 {
  0%   { transform: translate(0px, 0px) scale(1); opacity: 0.45; }
  40%  { transform: translate(-50px, -30px) scale(1.12); opacity: 0.52; }
  70%  { transform: translate(-20px, -55px) scale(0.92); opacity: 0.35; }
  100% { transform: translate(-60px, -15px) scale(1.08); opacity: 0.48; }
}

@keyframes fogDrift3 {
  0%   { transform: translate(0px, 0px) scale(1); opacity: 0.4; }
  50%  { transform: translate(35px, -40px) scale(1.15); opacity: 0.5; }
  100% { transform: translate(15px, -70px) scale(0.9); opacity: 0.32; }
}

/* ── Responsive ── */
@media (max-width: 768px) {
  .login-page  { flex-direction: column; }
  .form-side   { width: 100%; padding: 32px 20px; background: #ffffff; }
  .video-side  { width: 100%; padding: 0; }
  .hero-video  { height: 45vh; }
}
</style>