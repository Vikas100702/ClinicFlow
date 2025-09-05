import axios from "axios";

const API_URL = "http://localhost:8000";

// ✅ Axios instance
const api = axios.create({
  baseURL: API_URL,
});

// ✅ Request Interceptor for token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  // =========================
  // 🔹 USER REGISTRATION FLOW
  // =========================
  register: async (formData) => {
    // Step 1: Register user (common fields)
    const userPayload = {
      first_name: formData.first_name,
      last_name: formData.last_name,
      gender: formData.gender.toUpperCase(),
      email: formData.email,
      phone_number: formData.phone_number,
      role: formData.role.toUpperCase(),
      password: formData.password,
    };

    const userRes = await api.post("/register/user", userPayload);
    const newUser = userRes.data;

    // Step 2: If Doctor → call doctor API
    if (formData.role === "doctor") {
      await api.post("/register/doctor", {
        user_id: newUser.user_id,
        specialization: formData.specialization,
        qualification: formData.qualification,
        experience: formData.experience,
      });
    }

    // Step 2: If Patient → call patient API
    if (formData.role === "patient") {
      await api.post("/register/patient", {
        user_id: newUser.user_id,
        address: formData.address,
      });
    }

    return newUser; // ✅ Return final created user
  },

  // =========================
  // 🔹 LOGIN
  // =========================
  login: async (email, password) => {
    const response = await api.post("/auth/login", { email, password });
    localStorage.setItem("token", response.data.access_token);
    return response.data;
  },

  // =========================
  // 🔹 LOGOUT
  // =========================
  logout: () => {
    localStorage.removeItem("token");
  },

  // =========================
  // 🔹 CURRENT USER
  // =========================
  getCurrentUser: async () => {
    const response = await api.get("/auth/me");
    return response.data;
  },

  // 🔹 Extra: get all users (admin/debug)
  getAllUsers: async () => {
    const response = await api.get("/register/users");
    return response.data;
  },
};
