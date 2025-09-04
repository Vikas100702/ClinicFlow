// src/pages/Auth/Registration.jsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Register.css"; 
import { registerSchema } from "../../../utils/validation";

function Registration({ setUserData }) {
  const [role, setRole] = useState("patient");
  const [formData, setFormData] = useState({
    fullName: "",
    email: "",
    mobile: "",
    address: "",
    age: "",
    qualification: "",
    specialist: "",
    experience: ""
  });

  const navigate = useNavigate();

  // Handle input change
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Submit form
  const handleSubmit = (e) => {
    e.preventDefault();
    const finalData = { ...formData, role };
    setUserData(finalData);
    console.log("Registration Data:", finalData);
    navigate("/profile"); // 🔥 Redirect after submit
  };

  return (
    <div className="register-container">
      <h2 className="register-title">Create an Account</h2>
      <form className="register-form" onSubmit={handleSubmit}>

        {/* Role Selection */}
        <div className="form-group">
          <label>Select Role:</label>
          <select
            name="role"
            value={role}
            onChange={(e) => setRole(e.target.value)}
          >
            <option value="patient">Patient</option>
            <option value="doctor">Doctor</option>
          </select>
        </div>

        {/* Common Fields */}
        <div className="form-group">
          <label>Full Name:</label>
          <input
            type="text"
            name="fullName"
            value={formData.fullName}
            onChange={handleChange}
            placeholder="Enter Full Name"
            required
          />
        </div>

        <div className="form-group">
          <label>Email:</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="Enter Email"
            required
          />
        </div>

        <div className="form-group">
          <label>Mobile Number:</label>
          <input
            type="tel"
            name="mobile"
            value={formData.mobile}
            onChange={handleChange}
            placeholder="Enter Mobile Number"
            required
          />
        </div>

        <div className="form-group">
          <label>Address:</label>
          <textarea
            name="address"
            value={formData.address}
            onChange={handleChange}
            placeholder="Enter Address"
            required
          />
        </div>

        {/* Patient Specific */}
        {role === "patient" && (
          <div className="form-group">
            <label>Age:</label>
            <input
              type="number"
              name="age"
              value={formData.age}
              onChange={handleChange}
              placeholder="Enter Age"
              required
            />
          </div>
        )}

        {/* Doctor Specific */}
        {role === "doctor" && (
          <>
            <div className="form-group">
              <label>Qualification:</label>
              <input
                type="text"
                name="qualification"
                value={formData.qualification}
                onChange={handleChange}
                placeholder="Enter Qualification"
                required
              />
            </div>
            <div className="form-group">
              <label>Specialist:</label>
              <input
                type="text"
                name="specialist"
                value={formData.specialist}
                onChange={handleChange}
                placeholder="Enter Specialist Area"
                required
              />
            </div>
            <div className="form-group">
              <label>Experience (in years):</label>
              <input
                type="number"
                name="experience"
                value={formData.experience}
                onChange={handleChange}
                placeholder="Enter Experience"
                required
              />
            </div>
          </>
        )}

        {/* Submit */}
        <button type="submit" className="submit-btn">
          Register
        </button>
      </form>
    </div>
  );
}

export default Registration;