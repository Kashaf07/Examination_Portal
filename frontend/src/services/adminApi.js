// src/services/adminApi.js
import axios from "axios";

const API_BASE = "http://localhost:5000/api";

// ------------------------------
// Axios Instance
// ------------------------------
const api = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
});

// ------------------------------
// Utility wrapper for clean calls
// ------------------------------
async function callApi(apiFunc) {
  try {
    const res = await apiFunc();
    return { success: true, data: res.data };
  } catch (err) {
    return {
      success: false,
      error: err.response?.data?.error || err.response?.data?.message || err.message,
    };
  }
}

// ======================================================================
// 🟦 SCHOOLS API
// ======================================================================
export const schoolsApi = {
  getAll: () => callApi(() => api.get("/admin/schools")),

  add: (payload) => callApi(() => api.post("/admin/schools", payload)),

  update: (id, payload) =>
    callApi(() => api.put(`/admin/schools/${id}`, payload)),

  delete: (id) => callApi(() => api.delete(`/admin/schools/${id}`)),
};

// ======================================================================
// 🟩 FACULTY API
// ======================================================================
export const facultyApi = {
  getAll: () => callApi(() => api.get("/admin/faculty")),

  add: (payload) => callApi(() => api.post("/admin/faculty", payload)),

  update: (id, payload) =>
    callApi(() => api.put(`/admin/faculty/${id}`, payload)),

  delete: (id) => callApi(() => api.delete(`/admin/faculty/${id}`)),
};

// ======================================================================
// 🟧 APPLICANTS API
// ======================================================================
export const applicantsApi = {
  getAll: () => callApi(() => api.get("/admin/applicants")),

  add: (payload) =>
    callApi(() => api.post(`/applicants/add`, payload)),

  delete: (id) => callApi(() => api.delete(`/admin/applicants/${id}`)),

  bulkDelete: (ids) =>
    callApi(() => api.post(`/admin/applicants/bulk-delete`, { applicant_ids: ids })),

  uploadFile: (formData) =>
    callApi(() =>
      api.post("/applicants/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
    ),
};

// ======================================================================
// 🟨 ADMINS API
// ======================================================================
export const adminsApi = {
  getAll: () => callApi(() => api.get("/admin/admins")),

  add: (payload) => callApi(() => api.post("/admin/admins", payload)),

  update: (id, payload) =>
    callApi(() => api.put(`/admin/admins/${id}`, payload)),

  delete: (id) => callApi(() => api.delete(`/admin/admins/${id}`)),
};

// ======================================================================
// 🟪 EXAMS API
// ======================================================================
export const examsApi = {
  getCreated: (adminEmail) =>
    callApi(() => api.get(`/exam/get_exams/${adminEmail}`)),

  create: (payload) => callApi(() => api.post("/exam/create", payload)),

  delete: (id) => callApi(() => api.delete(`/admin/exam/delete/${id}`)),

  getConducted: () => callApi(() => api.get(`/admin/conducted_exams`)),
};

// ======================================================================
// 🟫 LOGIN LOGS API
// ======================================================================
export const logsApi = {
  getAll: () => callApi(() => api.get("/admin/logs")),
};

// ======================================================================
// 🔻 AUTH / LOGOUT
// ======================================================================
export const authApi = {
  logout: (email, role) =>
    callApi(() => api.post("/auth/logout", { email, role })),
};
