<template>
  <router-view />

  <!-- 🔔 Warning Popup -->
  <div v-if="showWarning && $route.path !== '/'" class="session-warning">
    <div class="warning-box">
      <h2>Session Expiring</h2>
      <p>Your session will expire in <b :class="{ 'countdown-red': countdown <= 5 }">{{ countdown }} {{ countdown === 1 ? 'second' : 'seconds' }}</b> due to inactivity.</p>

      <button class="stay-btn" @click="stayLoggedIn">
        Stay Logged In
      </button>
    </div>
  </div>
</template>

<script>
import axios from "@/utils/axiosInstance";

export default {
  name: "App",

  data() {
    return {
      idleTimer: null,
      warningTimer: null,
      countdownTimer: null,
      timeout: 1 * 60 * 1000,        // 1 min
      warningTime: 30 * 1000, //4.5 * 60 * 1000,  // 4.5 mins
      showWarning: false,
      countdown: 30
    };
  },

  // Add this inside your export default, alongside methods/data
  watch: {
    $route(to) {
      if (to.path === '/') {
        this.showWarning = false;
        clearTimeout(this.idleTimer);
        clearTimeout(this.warningTimer);
      }
    }
  },

  // Add this inside your export default, alongside methods/data
  watch: {
    $route(to) {
      if (to.path === '/') {
        this.showWarning = false;
        clearTimeout(this.idleTimer);
        clearTimeout(this.warningTimer);
      }
    }
  },

  methods: {
    resetTimer() {
      const token = localStorage.getItem("token");
      const currentPath = this.$route.path; // ✅ FIXED

      // ❌ DO NOT RUN on login page
      if (!token || currentPath === "/") return;

      clearTimeout(this.idleTimer);
      clearTimeout(this.warningTimer);
      clearInterval(this.countdownTimer);

      this.showWarning = false;
      this.countdown = 30;

      // ⏳ Warning before logout
      this.warningTimer = setTimeout(() => {
        this.showWarning = true;
        this.startCountdown();
      }, this.warningTime);

      // ⛔ Final logout
      this.idleTimer = setTimeout(() => {
        this.logoutUser();
      }, this.timeout);
    },

    startCountdown() {
      this.countdown = 30;
      this.countdownTimer = setInterval(() => {
        this.countdown--;
        if (this.countdown <= 0) {
          clearInterval(this.countdownTimer);
        }
      }, 1000);
    },

    stayLoggedIn() {
      this.showWarning = false;
      clearInterval(this.countdownTimer);
      this.countdown = 30;
      this.resetTimer(); // 🔁 Reset timers again
    },

    async logoutUser() {
      const token = localStorage.getItem("token");
      if (!token) return;

      try {
        await axios.post(
          "/auth/logout",
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );
        console.log("✅ Logout saved in DB");
        
      } catch (e) {
        console.log("Logout API failed (safe to ignore)", e);
      }

      // ❌ stop timers
      clearTimeout(this.idleTimer);
      clearTimeout(this.warningTimer);
      clearInterval(this.countdownTimer);

      this.showWarning = false;

      // ❌ clear session
      localStorage.clear();

      // ✅ redirect
      localStorage.setItem("session_expired", "true");
      this.$router.replace("/");
    }
  },

  mounted() {
    const events = ["mousemove", "keydown", "click", "scroll"];

    events.forEach(event => {
      window.addEventListener(event, this.resetTimer);
    });

    if (localStorage.getItem("token")) {
      this.resetTimer();
    }
  },

  beforeUnmount() {
    const events = ["mousemove", "keydown", "click", "scroll"];

    events.forEach(event => {
      window.removeEventListener(event, this.resetTimer);
    });

    clearTimeout(this.idleTimer);
    clearTimeout(this.warningTimer);
    clearInterval(this.countdownTimer);
  }
};
</script>

<style scoped>
.session-warning {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(15, 23, 42, 0.4);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.warning-box {
  background: #ffffff;
  padding: 40px 45px;
  border-radius: 18px;
  text-align: center;
  width: 360px; /* 🔥 bigger */
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  animation: popupIn 0.25s ease;
}

.warning-box h2 {
  font-size: 20px;
  font-weight: 700; /* 🔥 bold */
  color: #1e293b;
  margin-bottom: 12px;
}

.warning-box p {
  font-size: 14px;
  color: #475569;
  margin-bottom: 25px;
}

.stay-btn {
  background: #3b82f6; /* 🔥 blue-500 */
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  transition: 0.2s;
}

.stay-btn:hover {
  background: #2563eb;
  transform: translateY(-1px);
}

@keyframes popupIn {
  from {
    transform: scale(0.9);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes heartbeat {
  0%, 100% {
    transform: scale(1);
  }
  25% {
    transform: scale(1.1);
  }
  50% {
    transform: scale(1);
  }
  75% {
    transform: scale(1.05);
  }
}

.heartbeat-animation {
  animation: heartbeat 0.8s ease-in-out infinite;
}

.countdown-red {
  color: #ef4444 !important; /* red-500 */
  font-weight: 700;
}
</style>