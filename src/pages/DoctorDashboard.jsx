import React, { useEffect, useState } from "react";
import { Link, NavLink } from "react-router-dom";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  LineChart,
  Line,
} from "recharts";

const DoctorDashboard = () => {
  const [stats, setStats] = useState({
    patients: 0,
    appointments: 0,
    labOrders: 0,
    prescriptions: 0,
  });

  const [recentAppointments, setRecentAppointments] = useState([]);

  const appointmentData = [
    { day: "Mon", count: 5 },
    { day: "Tue", count: 8 },
    { day: "Wed", count: 6 },
    { day: "Thu", count: 10 },
    { day: "Fri", count: 7 },
  ];

  const labOrderData = [
    { day: "Mon", orders: 3 },
    { day: "Tue", orders: 4 },
    { day: "Wed", orders: 2 },
    { day: "Thu", orders: 5 },
    { day: "Fri", orders: 3 },
  ];

  useEffect(() => {
    // Mock data (replace with API later)
    setStats({
      patients: 120,
      appointments: 8,
      labOrders: 4,
      prescriptions: 15,
    });

    setRecentAppointments([
      { id: 1, name: "John Doe", date: "2025-08-22", time: "10:00 AM" },
      { id: 2, name: "Jane Smith", date: "2025-08-23", time: "11:30 AM" },
      { id: 3, name: "David Lee", date: "2025-08-23", time: "2:00 PM" },
    ]);
  }, []);

  return (
    <div className="flex">
      {/* Sidebar */}
      <aside className="w-64 bg-gray-800 text-white min-h-screen p-4">
        <h2 className="text-xl font-bold mb-6">Doctor Panel</h2>
        <nav className="flex flex-col gap-3">
          <NavLink
            to="/doctor-dashboard"
            className={({ isActive }) =>
              `px-3 py-2 rounded-lg ${
                isActive ? "bg-blue-500" : "hover:bg-gray-700"
              }`
            }
          >
            Dashboard
          </NavLink>
          <NavLink
            to="/patients"
            className={({ isActive }) =>
              `px-3 py-2 rounded-lg ${
                isActive ? "bg-blue-500" : "hover:bg-gray-700"
              }`
            }
          >
            Patients
          </NavLink>
          <NavLink
            to="/appointments"
            className={({ isActive }) =>
              `px-3 py-2 rounded-lg ${
                isActive ? "bg-blue-500" : "hover:bg-gray-700"
              }`
            }
          >
            Appointments
          </NavLink>
          <NavLink
            to="/lab-tests"
            className={({ isActive }) =>
              `px-3 py-2 rounded-lg ${
                isActive ? "bg-blue-500" : "hover:bg-gray-700"
              }`
            }
          >
            Lab Orders
          </NavLink>
        </nav>
      </aside>

      {/* Main Dashboard */}
      <div className="flex-1 p-6">
        <h1 className="text-2xl font-bold mb-6">Doctor Dashboard</h1>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-blue-100 p-4 rounded-lg shadow">
            <h2 className="text-lg font-semibold">Patients</h2>
            <p className="text-2xl font-bold">{stats.patients}</p>
          </div>
          <div className="bg-green-100 p-4 rounded-lg shadow">
            <h2 className="text-lg font-semibold">Appointments</h2>
            <p className="text-2xl font-bold">{stats.appointments}</p>
          </div>
          <div className="bg-yellow-100 p-4 rounded-lg shadow">
            <h2 className="text-lg font-semibold">Lab Orders</h2>
            <p className="text-2xl font-bold">{stats.labOrders}</p>
          </div>
          <div className="bg-purple-100 p-4 rounded-lg shadow">
            <h2 className="text-lg font-semibold">Prescriptions</h2>
            <p className="text-2xl font-bold">{stats.prescriptions}</p>
          </div>
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {/* Appointments per Day */}
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-bold mb-4">Appointments per Day</h2>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={appointmentData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Lab Orders Trend */}
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-bold mb-4">Lab Orders Trend</h2>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={labOrderData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="orders" stroke="#10b981" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Recent Appointments */}
        <div className="bg-white p-6 rounded-lg shadow mb-8">
          <h2 className="text-xl font-bold mb-4">Recent Appointments</h2>
          <table className="w-full text-left border-collapse">
            <thead>
              <tr>
                <th className="border-b p-2">Patient Name</th>
                <th className="border-b p-2">Date</th>
                <th className="border-b p-2">Time</th>
              </tr>
            </thead>
            <tbody>
              {recentAppointments.map((appt) => (
                <tr key={appt.id}>
                  <td className="border-b p-2">{appt.name}</td>
                  <td className="border-b p-2">{appt.date}</td>
                  <td className="border-b p-2">{appt.time}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Quick Actions */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">Quick Actions</h2>
          <div className="flex flex-wrap gap-4">
            <Link
              to="/create-prescription"
              className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
            >
              Create Prescription
            </Link>
            <Link
              to="/patients"
              className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600"
            >
              View Patients
            </Link>
            <Link
              to="/lab-tests"
              className="bg-yellow-500 text-white px-4 py-2 rounded-lg hover:bg-yellow-600"
            >
              Lab Orders
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DoctorDashboard;
