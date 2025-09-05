import api from './api'

export const cmhAPI = {
  getSummary: (patientId) => {
    return api.get(`/cmh/${patientId}/summary`).then(res => res.data)
  },
  
  getTimeline: (patientId, params = {}) => {
    return api.get(`/cmh/${patientId}/timeline`, { params }).then(res => res.data)
  },
  
  // Allergy endpoints
  getAllergies: (patientId) => {
    return api.get(`/cmh/${patientId}/allergies`).then(res => res.data)
  },
  
  createAllergy: (patientId, allergyData) => {
    return api.post(`/cmh/${patientId}/allergies`, allergyData).then(res => res.data)
  },
  
  updateAllergy: (allergyId, allergyData) => {
    return api.patch(`/cmh/allergies/${allergyId}`, allergyData).then(res => res.data)
  },
  
  // Condition endpoints
  getConditions: (patientId) => {
    return api.get(`/cmh/${patientId}/conditions`).then(res => res.data)
  },
  
  createCondition: (patientId, conditionData) => {
    return api.post(`/cmh/${patientId}/conditions`, conditionData).then(res => res.data)
  },
  
  // Medication endpoints
  getMedications: (patientId) => {
    return api.get(`/cmh/${patientId}/medications`).then(res => res.data)
  },
  
  createMedication: (patientId, medicationData) => {
    return api.post(`/cmh/${patientId}/medications`, medicationData).then(res => res.data)
  },
  
  // Vitals endpoints
  getVitals: (patientId) => {
    return api.get(`/cmh/${patientId}/vitals`).then(res => res.data)
  },
  
  createVital: (patientId, vitalData) => {
    return api.post(`/cmh/${patientId}/vitals`, vitalData).then(res => res.data)
  }
}
