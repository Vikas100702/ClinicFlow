import React, { useState } from "react";
import { registerSchema } from "../../../utils/validation.js";
import { authAPI } from "../../../services/auth.js";
import { useNavigate } from "react-router-dom";
import "./Register.css";

const Registration = () => {
  const [formData, setFormData] = useState({
    role: "",
    first_name: "",
    last_name: "",
    gender: "MALE", // 👈 default required hai backend ke liye
    email: "",
    phone_number: "",
    password: "",
    confirmPassword: "",
    address: "",
    qualification: "",
    specialization: "",
    experience: "",
  });

  const [errors, setErrors] = useState({});
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const validationErrors = registerSchema(formData);
    setErrors(validationErrors);

    if (Object.keys(validationErrors).length > 0) return;

    try {
      const response = await authAPI.register(formData);
      console.log("✅ Registration Response:", response);

      setMessage("✅ Registration successful! Please login.");
      setTimeout(() => navigate("/login"), 1500);
    } catch (error) {
      console.error("❌ Registration error:", error);
      const backendErrors = error.response?.data?.detail;

      // backend se agar list of errors aati hai
      if (Array.isArray(backendErrors)) {
        setMessage(backendErrors.map((err) => err.msg).join(", "));
      } else {
        setMessage(backendErrors || "❌ Registration failed");
      }
    }
  };

  return (
    <div className="register-container">
      <form className="register-form" onSubmit={handleSubmit}>
        <h2 className="register-title">Register</h2>
        {message && <p className="status-msg">{message}</p>}

        {/* Role Selection Always First */}
        <div className="form-group">
          <label>Select Role</label>
          <select name="role" value={formData.role} onChange={handleChange}>
            <option value="">-- Select Role --</option>
            <option value="patient">Patient</option>
            <option value="doctor">Doctor</option>
          </select>
          {errors.role && <p className="error">{errors.role}</p>}
        </div>

        {/* Show rest of form only when role is selected */}
        {formData.role && (
          <div className="fade-in">
            {/* Name Row */}
            <div className="form-row">
              <div className="form-group">
                <input
                  type="text"
                  name="first_name"
                  placeholder="First Name"
                  value={formData.first_name}
                  onChange={handleChange}
                />
                {errors.first_name && (
                  <p className="error">{errors.first_name}</p>
                )}
              </div>
              <div className="form-group">
                <input
                  type="text"
                  name="last_name"
                  placeholder="Last Name"
                  value={formData.last_name}
                  onChange={handleChange}
                />
                {errors.last_name && <p className="error">{errors.last_name}</p>}
              </div>
            </div>

            {/* Gender */}
            <div className="form-group">
              <label>Gender</label>
              <select name="gender" value={formData.gender} onChange={handleChange}>
                <option value="MALE">Male</option>
                <option value="FEMALE">Female</option>
                <option value="OTHER">Other</option>
              </select>
            </div>

            {/* Email */}
            <div className="form-group">
              <input
                type="email"
                name="email"
                placeholder="Email"
                value={formData.email}
                onChange={handleChange}
              />
              {errors.email && <p className="error">{errors.email}</p>}
            </div>

            {/* Mobile */}
            <div className="form-group">
              <input
                type="text"
                name="phone_number"
                placeholder="Mobile"
                value={formData.phone_number}
                onChange={handleChange}
              />
              {errors.phone_number && (
                <p className="error">{errors.phone_number}</p>
              )}
            </div>

            {/* Password / Confirm Password */}
            <div className="form-row">
              <div className="form-group">
                <input
                  type="password"
                  name="password"
                  placeholder="Password"
                  value={formData.password}
                  onChange={handleChange}
                  autoComplete="new-password"
                />
                {errors.password && <p className="error">{errors.password}</p>}
              </div>
              <div className="form-group">
                <input
                  type="password"
                  name="confirmPassword"
                  placeholder="Confirm Password"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  autoComplete="new-password"
                />
                {errors.confirmPassword && (
                  <p className="error">{errors.confirmPassword}</p>
                )}
              </div>
            </div>

            {/* Patient-specific fields */}
            {formData.role === "patient" && (
              <div className="form-group fade-in">
                <input
                  type="text"
                  name="address"
                  placeholder="Address"
                  value={formData.address}
                  onChange={handleChange}
                />
                {errors.address && <p className="error">{errors.address}</p>}
              </div>
            )}

            {/* Doctor-specific fields */}
            {formData.role === "doctor" && (
              <div className="fade-in">
                <div className="form-group">
                  <input
                    type="text"
                    name="qualification"
                    placeholder="Qualification"
                    value={formData.qualification}
                    onChange={handleChange}
                  />
                  {errors.qualification && (
                    <p className="error">{errors.qualification}</p>
                  )}
                </div>

                <div className="form-group">
                  <input
                    type="text"
                    name="specialization"
                    placeholder="Specialist"
                    value={formData.specialization}
                    onChange={handleChange}
                  />
                  {errors.specialization && (
                    <p className="error">{errors.specialization}</p>
                  )}
                </div>

                <div className="form-group">
                  <input
                    type="number"
                    name="experience"
                    placeholder="Experience (years)"
                    value={formData.experience}
                    onChange={handleChange}
                  />
                  {errors.experience && (
                    <p className="error">{errors.experience}</p>
                  )}
                </div>
              </div>
            )}

            <button type="submit" className="submit-btn">
              Register
            </button>
          </div>
        )}
      </form>
    </div>
  );
};

export default Registration;
