import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'
import { appointmentsAPI } from '../../services/appointments'
import { cmhAPI } from '../../services/cmh'
import './Dashboard.css'

const PatientDashboard = () => {
  const { user } = useAuth()
  const [appointments, setAppointments] = useState([])
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [apptsResponse, summaryResponse] = await Promise.all([
          appointmentsAPI.getAppointments({ limit: 5 }),
          cmhAPI.getSummary(user.id)
        ])
        
        setAppointments(apptsResponse)
        setSummary(summaryResponse)
      } catch (error) {
        console.error('Error fetching dashboard data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [user.id])

  if (loading) {
    return <div>Loading...</div>
  }

  return (
    <div className="dashboard">
      <h1>Welcome, {user.full_name}</h1>
      
      <div className="dashboard-grid">
        <div className="dashboard-card">
          <h3>Upcoming Appointments</h3>
          {appointments.length > 0 ? (
            <ul className="appointment-list">
              {appointments.map(appt => (
                <li key={appt.id} className="appointment-item">
                  <div className="appointment-info">
                    <strong>Dr. {appt.doctor.user.full_name}</strong>
                    <span>{new Date(appt.start_time).toLocaleDateString()}</span>
                  </div>
                  <span className={`status-badge ${appt.status}`}>
                    {appt.status}
                  </span>
                </li>
              ))}
            </ul>
          ) : (
            <p>No upcoming appointments</p>
          )}
          <Link to="/appointments" className="btn btn-secondary">
            View All Appointments
          </Link>
        </div>

        <div className="dashboard-card">
          <h3>Medical Summary</h3>
          {summary && (
            <div className="summary-stats">
              <div className="stat-item">
                <span className="stat-number">{summary.allergies.length}</span>
                <span className="stat-label">Allergies</span>
              </div>
              <div className="stat-item">
                <span className="stat-number">{summary.conditions.length}</span>
                <span className="stat-label">Conditions</span>
              </div>
              <div className="stat-item">
                <span className="stat-number">{summary.medications.length}</span>
                <span className="stat-label">Medications</span>
              </div>
            </div>
          )}
          <Link to="/cmh-summary" className="btn btn-secondary">
            View Full Summary
          </Link>
        </div>

        <div className="dashboard-card">
          <h3>Quick Actions</h3>
          <div className="action-buttons">
            <Link to="/appointments" className="btn btn-primary">
              Book Appointment
            </Link>
            <Link to="/doctors" className="btn btn-primary">
              Find Doctors
            </Link>
            <Link to="/cmh-timeline" className="btn btn-primary">
              View Timeline
            </Link>
            {/* 🔥 New Link for Prescriptions */}
            <Link to="/prescriptions" className="btn btn-primary">
              My Prescriptions
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PatientDashboard
