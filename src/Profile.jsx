// src/pages/Auth/Profile.jsx
import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import "./Profile.css";

const Profile = () => {
  const location = useLocation();
  const { userData, userType } = location.state || {};
  const [profile, setProfile] = useState({});
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    if (userType === "patient") {
      setProfile({
        fullName: userData.fullName,
        email: userData.email,
        mobile: userData.mobile,
        address: userData.address,
        age: userData.age || ""
      });
    } else if (userType === "doctor") {
      setProfile({
        fullName: userData.fullName,
        email: userData.email,
        mobile: userData.mobile,
        address: userData.address,
        specialization: userData.specialization,
        experience: userData.experience,
        fees: userData.fees
      });
    }
  }, [userType, userData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProfile({ ...profile, [name]: value });
  };

  const handleSave = () => {
    setIsEditing(false);
    alert("Profile updated successfully ✅");
    console.log("Updated Profile:", profile);
  };

  if (!userData) {
    return <h2>No Profile Data Found</h2>;
  }

  return (
    <div className="profile-container">
      <div className="profile-card">
        <h2>{userType === "patient" ? "Patient Profile" : "Doctor Profile"}</h2>

        <p><strong>Full Name:</strong> {profile.fullName}</p>
        <p><strong>Email:</strong> {profile.email}</p>
        <p><strong>Mobile:</strong> {profile.mobile}</p>
        <p><strong>Address:</strong> {profile.address}</p>

        {userType === "patient" && (
          <p>
            <strong>Age:</strong>{" "}
            {isEditing ? (
              <input type="number" name="age" value={profile.age} onChange={handleChange} />
            ) : (
              profile.age
            )}
          </p>
        )}

        {userType === "doctor" && (
          <>
            <p><strong>Specialization:</strong> {profile.specialization}</p>
            <p>
              <strong>Experience:</strong>{" "}
              {isEditing ? (
                <input type="number" name="experience" value={profile.experience} onChange={handleChange} />
              ) : (
                `${profile.experience} years`
              )}
            </p>
            <p>
              <strong>Consultation Fees:</strong>{" "}
              {isEditing ? (
                <input type="number" name="fees" value={profile.fees} onChange={handleChange} />
              ) : (
                `₹${profile.fees}`
              )}
            </p>
          </>
        )}

        <div className="profile-actions">
          {isEditing ? (
            <button className="save-btn" onClick={handleSave}>Save</button>
          ) : (
            <button className="edit-btn" onClick={() => setIsEditing(true)}>Edit</button>
          )}
        </div>
      </div>
    </div>
  );
};

export default Profile;
