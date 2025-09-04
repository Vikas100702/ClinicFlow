// frontend/src/services/apis/prescriptions.js
import api from "../api"; // axios instance

export const prescriptionsAPI = {
  // Fetch logged-in patient's prescriptions
  async getMyPrescriptions() {
    const res = await api.get("/prescriptions/my/");
    return res.data;
  },

  // Download prescription PDF
  async downloadPdf(id) {
    const res = await api.get(`/prescriptions/${id}/pdf/`, {
      responseType: "blob",
    });
    return res.data;
  },

  // Create new prescription
  async create(data) {
    const res = await api.post("/prescriptions/", data);
    return res.data;
  },
};
