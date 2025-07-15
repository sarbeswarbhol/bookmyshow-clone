// src/api/api.js
import axios from "axios";

// ===============================
// 🔧 Base URL Setup
// ===============================
const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/";

// ===============================
// 🔓 Public API Instance
// ===============================
const publicAPI = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// ===============================
// 🔐 Authenticated API Instance
// ===============================
const authAPI = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// === Attach Access Token ===
authAPI.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// === Auto-refresh Access Token ===
authAPI.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const refresh = localStorage.getItem("refresh");

    if (error.response?.status === 401 && refresh && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const res = await publicAPI.post("users/token/refresh/", { refresh });
        const newAccess = res.data.access;
        localStorage.setItem("access", newAccess);
        originalRequest.headers.Authorization = `Bearer ${newAccess}`;
        return authAPI(originalRequest); // Retry with new token
      } catch (refreshErr) {
        localStorage.clear();
        window.location.href = "/login";
        return Promise.reject(refreshErr);
      }
    }

    return Promise.reject(error);
  }
);


export { publicAPI, authAPI };
