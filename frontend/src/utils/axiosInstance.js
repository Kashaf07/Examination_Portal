import axios from 'axios';

const instance = axios.create({
  baseURL: `http://${window.location.hostname}:5000/api`,
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
