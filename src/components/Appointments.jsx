import React, { useState } from 'react';

const Appointments = () => {
  const [appointments, setAppointments] = useState([
    { id: 1, name: 'John Doe', date: '2025-08-22', time: '10:30 AM' },
    { id: 2, name: 'Jane Smith', date: '2025-08-23', time: '02:00 PM' }
  ]);

  const [newAppointment, setNewAppointment] = useState({
    name: '',
    date: '',
    time: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewAppointment({ ...newAppointment, [name]: value });
  };

  const handleAdd = (e) => {
    e.preventDefault();
    if (!newAppointment.name || !newAppointment.date || !newAppointment.time) return;
    
    setAppointments([
      ...appointments,
      { id: appointments.length + 1, ...newAppointment }
    ]);

    setNewAppointment({ name: '', date: '', time: '' });
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Appointments</h2>
      
      <ul>
        {appointments.map(app => (
          <li key={app.id}>
            {app.name} - {app.date} at {app.time}
          </li>
        ))}
      </ul>

      <h3>Add New Appointment</h3>
      <form onSubmit={handleAdd}>
        <input
          type="text"
          name="name"
          placeholder="Patient Name"
          value={newAppointment.name}
          onChange={handleChange}
          required
        />
        <input
          type="date"
          name="date"
          value={newAppointment.date}
          onChange={handleChange}
          required
        />
        <input
          type="time"
          name="time"
          value={newAppointment.time}
          onChange={handleChange}
          required
        />
        <button type="submit">Add Appointment</button>
      </form>
    </div>
  );
};

export default Appointments;
