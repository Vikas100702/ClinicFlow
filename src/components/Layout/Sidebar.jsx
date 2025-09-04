import React from "react";
import { NavLink } from "react-router-dom";
import {
  Home,
  CalendarDays,
  FileText,
  Users,
  Settings,
  LogOut,
  FlaskConical
} from "lucide-react";

import "./Sidebar.css";

const Sidebar = () => {
  const menuItems = [
    { name: "Dashboard", path: "/dashboard", icon: <Home size={20} /> },
    { name: "Appointments", path: "/appointments", icon: <CalendarDays size={20} /> },
    { name: "Case History", path: "/cmh", icon: <FileText size={20} /> },
    { name: "Lab Tests", path: "/lab-tests", icon: <FlaskConical size={20} /> },
    { name: "Patients", path: "/patients", icon: <Users size={20} /> },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>ClinicFlow</h2>
      </div>
      <nav className="sidebar-menu">
        {menuItems.map((item, index) => (
          <NavLink
            key={index}
            to={item.path}
            className={({ isActive }) =>
              `menu-item ${isActive ? "active" : ""}`
            }
          >
            {item.icon}
            <span>{item.name}</span>
          </NavLink>
        ))}
      </nav>
      <div className="sidebar-footer">
        <NavLink to="/settings" className="menu-item">
          <Settings size={20} />
          <span>Settings</span>
        </NavLink>
        <NavLink to="/logout" className="menu-item logout">
          <LogOut size={20} />
          <span>Logout</span>
        </NavLink>
      </div>
    </aside>
  );
};

export default Sidebar;
