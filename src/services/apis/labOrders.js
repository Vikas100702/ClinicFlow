import api from "../api"; // Axios instance

export const labOrdersAPI = {
  async getMyLabOrders() {
    const res = await api.get("/lab-orders/my/");
    return res.data;
  },

  async downloadPdf(id) {
    const res = await api.get(`/lab-orders/${id}/pdf/`, {
      responseType: "blob",
    });
    return res.data;
  },
};
