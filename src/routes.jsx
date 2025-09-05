import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './contexts/AuthContext'
import Layout from './components/Layout/Layout'
import Login from './pages/Auth/Login'
import Register from './pages/Auth/Register'
import PatientDashboard from './pages/Dashboard/PatientDashboard'
import DoctorDashboard from './pages/Dashboard/DoctorDashboard'
import Appointments from "./components/Appointments";
import Doctors from './pages/Doctors'
import Prescriptions from './pages/Prescriptions'
import LabOrders from './pages/LabOrders'
import CMHSummary from './pages/CMH/CMHSummary'
import CMHTimeline from './pages/CMH/CMHTimeline'

const ProtectedRoute = ({ children, requiredRole }) => {
  const { user, isAuthenticated } = useAuth()
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  
  if (requiredRole && user.role !== requiredRole && user.role !== 'admin') {
    return <Navigate to="/dashboard" replace />
  }
  
  return children
}

const AppRoutes = () => {
  const { user, isAuthenticated } = useAuth()
  
  return (
    <Routes>
      <Route 
        path="/login" 
        element={!isAuthenticated ? <Login /> : <Navigate to="/dashboard" replace />} 
      />
      <Route 
        path="/register" 
        element={!isAuthenticated ? <Register /> : <Navigate to="/dashboard" replace />} 
      />
      
      {isAuthenticated && (
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route 
            path="dashboard" 
            element={
              user.role === 'patient' ? <PatientDashboard /> : <DoctorDashboard />
            } 
          />
          <Route path="appointments" element={<Appointments />} />
          <Route path="doctors" element={<Doctors />} />
          <Route path="prescriptions" element={<Prescriptions />} />
          <Route path="lab-orders" element={<LabOrders />} />
          <Route path="cmh-summary" element={<CMHSummary />} />
          <Route path="cmh-timeline" element={<CMHTimeline />} />
          
          {/* Admin routes */}
          <Route 
            path="admin/*" 
            element={
              <ProtectedRoute requiredRole="admin">
                <div>Admin Panel</div>
              </ProtectedRoute>
            } 
          />
        </Route>
      )}
      
      <Route path="*" element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} replace />} />
    </Routes>
  )
}

export default AppRoutes
