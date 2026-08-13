import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api";

const api = axios.create({ baseURL: API_URL });

// Automatically attach the JWT (if present) to every outgoing request,
// so individual API calls don't need to handle auth headers manually.
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("gigboard_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
export default api;
