import React, { createContext, useContext, useState, useEffect } from "react";
import { authAPI } from "../services/auth";

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem("token"));

  useEffect(() => {
    if (token) {
      authAPI
        .getCurrentUser()
        .then((data) => {
          // data.message => "Hello, <user_id>! Your role is <role>."
          const parsed = parseProtectedMessage(data.message);
          setUser(parsed);
          setLoading(false);
        })
        .catch(() => {
          localStorage.removeItem("token");
          setToken(null);
          setUser(null);
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  }, [token]);

  const login = async (email, password) => {
    try {
      const { access_token } = await authAPI.login(email, password);
      localStorage.setItem("token", access_token);
      setToken(access_token);

      const data = await authAPI.getCurrentUser();
      const parsed = parseProtectedMessage(data.message);
      setUser(parsed);

      return { success: true };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || "Login failed",
      };
    }
  };

  const register = async (userData) => {
    try {
      await authAPI.register(userData);
      return { success: true };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || "Registration failed",
      };
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        register,
        logout,
        loading,
        isAuthenticated: !!user,
      }}
    >
      {!loading && children}
    </AuthContext.Provider>
  );
};

// Helper: Parse backend "Hello <id>! Your role is <role>."
function parseProtectedMessage(message) {
  const match = message.match(/Hello, (\d+)! Your role is (.+)\./);
  if (match) {
    return { id: match[1], role: match[2] };
  }
  return null;
}
