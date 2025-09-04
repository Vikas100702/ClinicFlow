import api from "../api"; // adjust path if needed

export const patientLabResultsAPI = {
  async getMyLabResults() {
    const res = await api.get("/lab-results/my/");
    return res.data;
  },

  async downloadPdf(id) {
    const res = await api.get(`/lab-results/${id}/pdf/`, {
      responseType: "blob",
    });
    return res.data;
  },
};
