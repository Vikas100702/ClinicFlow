import api from './api'

export const appointmentsAPI = {
  getAppointments: (params = {}) => {
    return api.get('/appointments', { params }).then(res => res.data)
  },
  
  getAppointment: (id) => {
    return api.get(`/appointments/${id}`).then(res => res.data)
  },
  
  createAppointment: (appointmentData) => {
    return api.post('/appointments', appointmentData).then(res => res.data)
  },
  
  updateAppointment: (id, appointmentData) => {
    return api.patch(`/appointments/${id}`, appointmentData).then(res => res.data)
  },
  
  cancelAppointment: (id) => {
    return api.patch(`/appointments/${id}`, { status: 'cancelled' }).then(res => res.data)
  }
}
