import axios from "axios";

const API_URL = "http://localhost:8000"; // Backend root (no /api prefix)

// Prescriptions API Service
export const prescriptionsAPI = {
  // Create a new prescription
  create: async (data) => {
    const res = await axios.post(`${API_URL}/prescriptions/`, data);
    return res.data;
  },

  // Get prescriptions by patient ID
  getByPatient: async (patientId) => {
    const res = await axios.get(`${API_URL}/prescriptions/patient/${patientId}`);
    return res.data;
  },

  // Get prescription by prescription ID
  getById: async (prescriptionId) => {
    const res = await axios.get(`${API_URL}/prescriptions/${prescriptionId}`);
    return res.data;
  },
};
