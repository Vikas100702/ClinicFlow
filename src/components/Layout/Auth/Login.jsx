import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom"; // ✅ For redirect
import { loginSchema } from "../../../utils/validation"; // ✅ Your validation
import "./Login.css";

const Login = () => {
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [errors, setErrors] = useState({});
  const [message, setMessage] = useState(""); // ✅ For success/error messages
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const validationErrors = loginSchema(formData);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:8000/login", formData, {
        headers: { "Content-Type": "application/json" },
      });

      // ✅ Save JWT token
      localStorage.setItem("token", response.data.access_token);

      setMessage("Login successful!");
      setErrors({});

      // ✅ Redirect after 1 second
      setTimeout(() => navigate("/dashboard"), 1000);
    } catch (error) {
      if (error.response) {
        setMessage(error.response.data.detail || "Login failed");
      } else {
        setMessage("Server error. Please try again.");
      }
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>Login</h2>
        {message && <p className="status-msg">{message}</p>} {/* ✅ Show message */}
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            name="email"
            placeholder="Enter your email"
            value={formData.email}
            onChange={handleChange}
          />
          {errors.email && <p className="error">{errors.email}</p>}

          <input
            type="password"
            name="password"
            placeholder="Enter your password"
            value={formData.password}
            onChange={handleChange}
            autoComplete="current-password"
          />
          {errors.password && <p className="error">{errors.password}</p>}

          <div className="forgot-password">
            <a href="/forgot-password">Forgot Password?</a>
          </div>

          <button type="submit" className="login-btn">
            Login
          </button>
        </form>
        <p>
          Don’t have an account? <a href="/register">Register</a>
        </p>
      </div>
    </div>
  );
};

export default Login;
