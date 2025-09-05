import { useState, useEffect } from 'react'
import { useAuth } from '../../contexts/AuthContext'
import { cmhAPI } from '../../services/cmh'
import './CMH.css'

const CMHSummary = () => {
  const { user } = useAuth()
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const data = await cmhAPI.getSummary(user.id)
        setSummary(data)
      } catch (error) {
        console.error('Error fetching CMH summary:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchSummary()
  }, [user.id])

  if (loading) {
    return <div>Loading...</div>
  }

  if (!summary) {
    return <div>Error loading medical summary</div>
  }

  return (
    <div className="cmh-container">
      <h1>Medical Summary</h1>
      
      <div className="cmh-sections">
        {/* Allergies Section */}
        <section className="cmh-section">
          <h2>Allergies</h2>
          {summary.allergies.length > 0 ? (
            <div className="items-grid">
              {summary.allergies.map(allergy => (
                <div key={allergy.id} className="cmh-item">
                  <h4>{allergy.substance}</h4>
                  <p>Reaction: {allergy.reaction || 'Not specified'}</p>
                  <p>Severity: {allergy.severity}</p>
                  <span className={`status-badge ${allergy.status}`}>
                    {allergy.status}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p>No allergies recorded</p>
          )}
        </section>

        {/* Conditions Section */}
        <section className="cmh-section">
          <h2>Medical Conditions</h2>
          {summary.conditions.length > 0 ? (
            <div className="items-grid">
              {summary.conditions.map(condition => (
                <div key={condition.id} className="cmh-item">
                  <h4>{condition.display}</h4>
                  <p>Status: {condition.status}</p>
                  {condition.onset_date && (
                    <p>Onset: {new Date(condition.onset_date).toLocaleDateString()}</p>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p>No medical conditions recorded</p>
          )}
        </section>

        {/* Medications Section */}
        <section className="cmh-section">
          <h2>Medications</h2>
          {summary.medications.length > 0 ? (
            <div className="items-grid">
              {summary.medications.map(medication => (
                <div key={medication.id} className="cmh-item">
                  <h4>{medication.drug_name}</h4>
                  <p>Dosage: {medication.dosage || 'Not specified'}</p>
                  <p>Frequency: {medication.frequency || 'Not specified'}</p>
                  <span className={`status-badge ${medication.status}`}>
                    {medication.status}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p>No medications recorded</p>
          )}
        </section>

        {/* Latest Vitals Section */}
        <section className="cmh-section">
          <h2>Latest Vitals</h2>
          {summary.latest_vitals ? (
            <div className="cmh-item">
              <div className="vitals-grid">
                {summary.latest_vitals.systolic_bp && summary.latest_vitals.diastolic_bp && (
                  <div className="vital-item">
                    <span className="vital-label">Blood Pressure</span>
                    <span className="vital-value">
                      {summary.latest_vitals.systolic_bp}/{summary.latest_vitals.diastolic_bp} mmHg
                    </span>
                  </div>
                )}
                {summary.latest_vitals.heart_rate && (
                  <div className="vital-item">
                    <span className="vital-label">Heart Rate</span>
                    <span className="vital-value">{summary.latest_vitals.heart_rate} bpm</span>
                  </div>
                )}
                {summary.latest_vitals.temp_c && (
                  <div className="vital-item">
                    <span className="vital-label">Temperature</span>
                    <span className="vital-value">{summary.latest_vitals.temp_c} °C</span>
                  </div>
                )}
                {summary.latest_vitals.spo2 && (
                  <div className="vital-item">
                    <span className="vital-label">SpO2</span>
                    <span className="vital-value">{summary.latest_vitals.spo2}%</span>
                  </div>
                )}
              </div>
              <p className="vital-date">
                Recorded on: {new Date(summary.latest_vitals.recorded_at).toLocaleDateString()}
              </p>
            </div>
          ) : (
            <p>No vitals recorded</p>
          )}
        </section>
      </div>
    </div>
  )
}

export default CMHSummary
