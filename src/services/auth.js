import axios from 'axios';

const API_URL = 'http://localhost:8000'; // FastAPI backend root

export const authAPI = {
  // User Registration
  registerUser: async (userData) => {
    const response = await axios.post(`${API_URL}/register/user`, userData);
    return response.data;
  },

  // Doctor Registration
  registerDoctor: async (doctorData) => {
    const response = await axios.post(`${API_URL}/register/doctor`, doctorData);
    return response.data;
  },

  // Patient Registration
  registerPatient: async (patientData) => {
    const response = await axios.post(`${API_URL}/register/patient`, patientData);
    return response.data;
  },

  // Get all Users
  getAllUsers: async () => {
    const response = await axios.get(`${API_URL}/register/users`);
    return response.data;
  }
};
