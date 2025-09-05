import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Sidebar from "./components/Layout/Sidebar.jsx";
import Login from "./components/Layout/Auth/Login.jsx";
import ForgotPassword from "./components/Layout/Auth/ForgotPassword.jsx";
import Register from "./components/Layout/Auth/Register.jsx";
import Dashboard from "./pages/Dashboard/DoctorDashboard.jsx";
import Appointments from "./components/Appointments.jsx";
import CMH from "./pages/CMH/CMHSummary.jsx";
import LabTests from "./contexts/LabOrders.jsx";
import LabOrders from "./contexts/LabOrders.jsx";
import Patients from "./pages/DoctorDashboard.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";
import { AuthProvider } from "./contexts/AuthContext.jsx";
import Profile from "./Profile.jsx";
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import CreatePrescriptionPage from "./pages/CreatePrescriptionPage.jsx";
import PatientPrescriptionsPage from "./pages/PatientPrescriptionsPage.jsx";
import PatientLabResultsPage from "./pages/PatientLabResultsPage.jsx";
import PatientDashboard from "./pages/Dashboard/PatientDashboard.jsx";


const PublicLayout = ({ children }) => (
  <div style={{ minHeight: "100vh", display: "flex", justifyContent: "center", alignItems: "center", backgroundColor: "#f7f9fc" }}>
    {children}
  </div>
);

const PrivateLayout = ({ children }) => (
  <div style={{ display: "flex", minHeight: "100vh" }}>
    <Sidebar />
    <div style={{ flex: 1, padding: "20px", backgroundColor: "#f7f9fc" }}>
      {children}
    </div>
  </div>
);

const App = () => {
  return (
    <AuthProvider>
      <ToastContainer />
      <Routes>
        {/* Default Redirect */}
        <Route path="/" element={<Navigate to="/login" />} />

        {/* Public Routes */}
        <Route
          path="/login"
          element={
            <PublicLayout>
              <Login />
            </PublicLayout>
          }
        />
        <Route
          path="/register"
          element={
            <PublicLayout>
              <Register />
            </PublicLayout>
          }
        />
        <Route
          path="/forgot-password"
          element={
            <PublicLayout>
              <ForgotPassword />
            </PublicLayout>
          }
        />

        {/* Protected Routes */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <PrivateLayout>
                <Dashboard />
              </PrivateLayout>
            </ProtectedRoute>
          }
        />
        <Route
  path="/PatientDashboard"
  element={
    <ProtectedRoute>
      <PrivateLayout>
        <PatientDashboard />
      </PrivateLayout>
    </ProtectedRoute>
  }
/>
        <Route
          path="/appointments"
          element={
            <ProtectedRoute>
              <PrivateLayout>
                <Appointments />
              </PrivateLayout>
            </ProtectedRoute>
          }
        />
        <Route
  path="/patient/lab-results"
  element={<PatientLabResultsPage />}
/>

        <Route
          path="/cmh"
          element={
            <ProtectedRoute>
              <PrivateLayout>
                <CMH />
              </PrivateLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/lab-tests"
          element={
            <ProtectedRoute>
              <PrivateLayout>
                <LabTests />
              </PrivateLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/patients"
          element={
            <ProtectedRoute>
              <PrivateLayout>
                <Patients />
              </PrivateLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <PrivateLayout>
                <Profile />
              </PrivateLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/patient/prescriptions"
          element={
            <ProtectedRoute>
              <PrivateLayout>
                <PatientPrescriptionsPage />
              </PrivateLayout>
            </ProtectedRoute>
          }
        />
        <Route
  path="/lab-orders"
  element={
    <ProtectedRoute>
      <PrivateLayout>
        <LabOrders />
      </PrivateLayout>
    </ProtectedRoute>
  }
/>
        <Route
          path="/patient/lab-results"
          element={
            <ProtectedRoute>
              <PrivateLayout>
                <PatientLabResultsPage />
              </PrivateLayout>
            </ProtectedRoute>
          }
        />
      </Routes>
    </AuthProvider>
  );
};

export default App;
