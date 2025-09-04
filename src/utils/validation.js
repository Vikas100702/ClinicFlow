// ✅ Validation for Registration Page
export const registerSchema = (formData) => {
  const errors = {};

  // First Name
  if (!formData.firstName?.trim()) {
    errors.firstName = "First Name is required";
  }

  // Last Name
  if (!formData.lastName?.trim()) {
    errors.lastName = "Last Name is required";
  }

  // Email
  if (!formData.email?.trim()) {
    errors.email = "Email is required";
  } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
    errors.email = "Invalid email format";
  }

  // Mobile
  if (!formData.mobile?.trim()) {
    errors.mobile = "Mobile number is required";
  } else if (!/^\d{10}$/.test(formData.mobile)) {
    errors.mobile = "Mobile must be 10 digits";
  }

  // Password
  if (!formData.password) {
    errors.password = "Password is required";
  } else if (formData.password.length < 6) {
    errors.password = "Password must be at least 6 characters";
  }

  // Confirm Password
  if (!formData.confirmPassword) {
    errors.confirmPassword = "Confirm Password is required";
  } else if (formData.password !== formData.confirmPassword) {
    errors.confirmPassword = "Passwords do not match";
  }

  // Role
  if (!formData.role) {
    errors.role = "Please select a role";
  }

  // Patient-specific field
  if (formData.role === "patient" && !formData.address?.trim()) {
    errors.address = "Address is required";
  }

  // Doctor-specific fields
  if (formData.role === "doctor") {
    if (!formData.qualification?.trim()) {
      errors.qualification = "Qualification is required";
    }
    if (!formData.specialist?.trim()) {
      errors.specialist = "Specialist is required";
    }
    if (!formData.experience?.toString().trim()) {
      errors.experience = "Experience is required";
    }
  }

  return errors;
};

// ✅ Validation for Login Page
export const loginSchema = (formData) => {
  const errors = {};

  // Email
  if (!formData.email?.trim()) {
    errors.email = "Email is required";
  } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
    errors.email = "Invalid email format";
  }

  // Password
  if (!formData.password) {
    errors.password = "Password is required";
  }

  return errors;
};

// ✅ Validation for Forgot Password Page
export const forgotPasswordSchema = (formData) => {
  const errors = {};

  // Email
  if (!formData.email?.trim()) {
    errors.email = "Email is required";
  } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
    errors.email = "Invalid email format";
  }

  return errors;
};
