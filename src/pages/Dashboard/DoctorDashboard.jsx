import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'
import { appointmentsAPI } from '../../services/appointments'
import { cmhAPI } from '../../services/cmh'
import './Dashboard.css'

const DoctorDashboard = () => {
  const { user } = useAuth()
  const [appointments, setAppointments] = useState([])
  const [patientSummaries, setPatientSummaries] = useState([])
  const [stats, setStats] = useState({
    totalAppointments: 0,
    completedAppointments: 0,
    pendingAppointments: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [apptsResponse, recentPatients] = await Promise.all([
          appointmentsAPI.getAppointments({ doctor_id: user.id, limit: 5 }),
          cmhAPI.getRecentPatients() // This would need to be implemented in the backend
        ])
        
        setAppointments(apptsResponse)
        
        // Calculate stats
        const total = apptsResponse.length
        const completed = apptsResponse.filter(a => a.status === 'completed').length
        const pending = apptsResponse.filter(a => ['booked', 'confirmed'].includes(a.status)).length
        
        setStats({
          totalAppointments: total,
          completedAppointments: completed,
          pendingAppointments: pending
        })
        
        // For demo purposes, we'll create some mock patient summaries
        const mockSummaries = [
          {
            id: 1,
            name: 'Patient One',
            lastVisit: '2023-05-15',
            conditions: ['Hypertension', 'Diabetes'],
            medications: 3
          },
          {
            id: 2,
            name: 'Patient Two',
            lastVisit: '2023-05-10',
            conditions: ['Asthma'],
            medications: 2
          }
        ]
        setPatientSummaries(mockSummaries)
      } catch (error) {
        console.error('Error fetching dashboard data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [user.id])

  const updateAppointmentStatus = async (appointmentId, status) => {
    try {
      await appointmentsAPI.updateAppointment(appointmentId, { status })
      // Refresh appointments
      const apptsResponse = await appointmentsAPI.getAppointments({ doctor_id: user.id, limit: 5 })
      setAppointments(apptsResponse)
    } catch (error) {
      console.error('Error updating appointment status:', error)
    }
  }

  if (loading) {
    return <div>Loading...</div>
  }

  return (
    <div className="dashboard">
      <h1>Welcome, Dr. {user.full_name}</h1>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Appointments</h3>
          <div className="stat-number">{stats.totalAppointments}</div>
        </div>
        <div className="stat-card">
          <h3>Completed</h3>
          <div className="stat-number">{stats.completedAppointments}</div>
        </div>
        <div className="stat-card">
          <h3>Pending</h3>
          <div className="stat-number">{stats.pendingAppointments}</div>
        </div>
      </div>
      
      <div className="dashboard-grid">
        <div className="dashboard-card">
          <h3>Today's Appointments</h3>
          {appointments.length > 0 ? (
            <ul className="appointment-list">
              {appointments.map(appt => (
                <li key={appt.id} className="appointment-item">
                  <div className="appointment-info">
                    <strong>{appt.patient.full_name}</strong>
                    <span>{new Date(appt.start_time).toLocaleTimeString()}</span>
                    <span>Reason: {appt.reason}</span>
                  </div>
                  <div className="appointment-actions">
                    <span className={`status-badge ${appt.status}`}>
                      {appt.status}
                    </span>
                    {appt.status === 'booked' && (
                      <button 
                        onClick={() => updateAppointmentStatus(appt.id, 'confirmed')}
                        className="btn btn-sm btn-primary"
                      >
                        Confirm
                      </button>
                    )}
                    {appt.status === 'confirmed' && (
                      <button 
                        onClick={() => updateAppointmentStatus(appt.id, 'completed')}
                        className="btn btn-sm btn-success"
                      >
                        Complete
                      </button>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <p>No appointments scheduled for today</p>
          )}
          <Link to="/appointments" className="btn btn-secondary">
            View All Appointments
          </Link>
        </div>

        <div className="dashboard-card">
          <h3>Recent Patients</h3>
          {patientSummaries.length > 0 ? (
            <ul className="patient-list">
              {patientSummaries.map(patient => (
                <li key={patient.id} className="patient-item">
                  <div className="patient-info">
                    <strong>{patient.name}</strong>
                    <span>Last visit: {new Date(patient.lastVisit).toLocaleDateString()}</span>
                  </div>
                  <div className="patient-details">
                    <span>Conditions: {patient.conditions.join(', ')}</span>
                    <span>Medications: {patient.medications}</span>
                  </div>
                  <Link 
                    to={`/cmh-summary?patientId=${patient.id}`} 
                    className="btn btn-sm btn-primary"
                  >
                    View Records
                  </Link>
                </li>
              ))}
            </ul>
          ) : (
            <p>No recent patients</p>
          )}
          <Link to="/cmh-summary" className="btn btn-secondary">
            View All Patients
          </Link>
        </div>

        <div className="dashboard-card">
          <h3>Quick Actions</h3>
          <div className="action-buttons">
            <Link to="/appointments" className="btn btn-primary">
              View Schedule
            </Link>
            <Link to="/cmh-summary" className="btn btn-primary">
              Patient Records
            </Link>
            <button className="btn btn-primary">
              Write Prescription
            </button>
            <button className="btn btn-primary">
              Order Lab Test
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DoctorDashboard
