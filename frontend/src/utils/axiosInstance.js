import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:5000/api', // ✅ NO trailing slash
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Attach token to every request if available
instance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default instance;
