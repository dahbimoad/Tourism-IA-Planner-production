import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FaEye, FaEyeSlash, FaCamera } from "react-icons/fa";

const Profil = () => {
  const [profile, setProfile] = useState({
    username: "JohnDoe",
    email: "john@example.com",
    avatar: "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?ixlib=rb-4.0.3",
    currentPassword: "",
    newPassword: ""
  });

  const [errors, setErrors] = useState({});
  const [showPassword, setShowPassword] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [imagePreview, setImagePreview] = useState(null);

  const validateUsername = (username) => {
    if (username.length < 3) return "Username must be at least 3 characters";
    if (username.length > 20) return "Username must be less than 20 characters";
    if (!/^[a-zA-Z0-9]+$/.test(username)) return "No special characters allowed";
    return "";
  };

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) return "Invalid email format";
    return "";
  };

  const validatePassword = (password) => {
    if (password.length < 8) return "Password must be at least 8 characters";
    if (!/[A-Z]/.test(password)) return "Password must include uppercase letter";
    if (!/[a-z]/.test(password)) return "Password must include lowercase letter";
    if (!/[0-9]/.test(password)) return "Password must include number";
    if (!/[!@#$%^&*]/.test(password)) return "Password must include special character";
    return "";
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        setErrors({ ...errors, avatar: "File size must be less than 5MB" });
        return;
      }
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSave = () => {
    const newErrors = {};

    // Validate username
    const usernameError = validateUsername(profile.username);
    if (usernameError) newErrors.username = usernameError;

    // Validate email
    const emailError = validateEmail(profile.email);
    if (emailError) newErrors.email = emailError;

    // Validate passwords if new password is provided
    if (profile.newPassword) {
      const passwordError = validatePassword(profile.newPassword);
      if (passwordError) newErrors.newPassword = passwordError;
      if (!profile.currentPassword) {
        newErrors.currentPassword = "Current password is required";
      }
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setIsSaving(true);

    // Simulate API call
    setTimeout(() => {
      setIsSaving(false);
      // Update profile with new avatar and clear passwords
      setProfile(prev => ({
        ...prev,
        avatar: imagePreview || prev.avatar,
        currentPassword: "",
        newPassword: ""
      }));
      setImagePreview(null);
    }, 1000);
  };

  const handleFieldChange = (field, value) => {
    setErrors({ ...errors, [field]: "" });
    setProfile({ ...profile, [field]: value });
  };

  return (
    <div className="pt-24">
        <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-4xl mx-auto p-6 bg-[#eef0ef] rounded-xl shadow-lg"
    >
      <div className="space-y-8">
        {/* Profile Picture Section */}
        <div className="flex flex-col items-center space-y-4">
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="relative"
          >
            <img
              src={imagePreview || profile.avatar}
              alt="Profile"
              className="w-32 h-32 rounded-full object-cover"
              onError={(e) => {
                e.target.src = "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?ixlib=rb-4.0.3";
              }}
            />
            <label
              htmlFor="avatar-upload"
              className="absolute bottom-0 right-0 bg-blue-500 p-2 rounded-full cursor-pointer hover:bg-blue-600 transition-colors"
            >
              <FaCamera className="text-white" />
              <input
                id="avatar-upload"
                type="file"
                className="hidden"
                accept="image/jpeg,image/png,image/webp"
                onChange={handleImageChange}
              />
            </label>
          </motion.div>
          {errors.avatar && (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-red-500 text-sm"
            >
              {errors.avatar}
            </motion.p>
          )}
        </div>

        {/* Profile Information Section */}
        <div className="space-y-6">
          {/* Username Field */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Username</label>
            <motion.input
              whileFocus={{ scale: 1.01 }}
              type="text"
              value={profile.username}
              onChange={(e) => handleFieldChange("username", e.target.value)}
              className={`mt-1 block w-full rounded-md border-gray-300 shadow-sm h-12 p-4 text-xl focus:border-blue-500 focus:ring-blue-500 ${
                errors.username ? 'border-red-500' : ''
              }`}
            />
            <AnimatePresence>
              {errors.username && (
                <motion.p
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  exit={{ opacity: 0, height: 0 }}
                  className="text-red-500 text-sm mt-1"
                >
                  {errors.username}
                </motion.p>
              )}
            </AnimatePresence>
          </div>

          {/* Email Field */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Email</label>
            <motion.input
              whileFocus={{ scale: 1.01 }}
              type="email"
              value={profile.email}
              onChange={(e) => handleFieldChange("email", e.target.value)}
              className={`mt-1 block w-full rounded-md border-gray-300 h-12 p-4 text-xl shadow-sm focus:border-blue-500 focus:ring-blue-500 ${
                errors.email ? 'border-red-500' : ''
              }`}
            />
            <AnimatePresence>
              {errors.email && (
                <motion.p
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  exit={{ opacity: 0, height: 0 }}
                  className="text-red-500 text-sm mt-1"
                >
                  {errors.email}
                </motion.p>
              )}
            </AnimatePresence>
          </div>

          {/* Password Change Section */}
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-gray-900">Change Password</h3>
            <div>
              <label className="block text-sm font-medium text-gray-700">Current Password</label>
              <div className="relative">
                <motion.input
                  whileFocus={{ scale: 1.01 }}
                  type={showPassword ? "text" : "password"}
                  value={profile.currentPassword}
                  onChange={(e) => handleFieldChange("currentPassword", e.target.value)}
                  className="mt-1 block w-full h-12 p-4 text-xl rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                >
                  {showPassword ? <FaEyeSlash /> : <FaEye />}
                </button>
              </div>
              {errors.currentPassword && (
                <motion.p
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="text-red-500 text-sm mt-1"
                >
                  {errors.currentPassword}
                </motion.p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">New Password</label>
              <div className="relative">
                <motion.input
                  whileFocus={{ scale: 1.01 }}
                  type={showPassword ? "text" : "password"}
                  value={profile.newPassword}
                  onChange={(e) => handleFieldChange("newPassword", e.target.value)}
                  className={`mt-1 block w-full rounded-md border-gray-300 h-12 p-4 text-xl shadow-sm focus:border-blue-500 focus:ring-blue-500 ${
                    errors.newPassword ? 'border-red-500' : ''
                  }`}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                >
                  {showPassword ? <FaEyeSlash /> : <FaEye />}
                </button>
              </div>
              <AnimatePresence>
                {errors.newPassword && (
                  <motion.p
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: "auto" }}
                    exit={{ opacity: 0, height: 0 }}
                    className="text-red-500 text-sm mt-1"
                  >
                    {errors.newPassword}
                  </motion.p>
                )}
              </AnimatePresence>
            </div>
          </div>
        </div>

        {/* Save Button */}
        <div className="flex justify-end">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleSave}
            disabled={isSaving}
            className={`px-6 py-2 rounded-md font-medium transition-colors ${
              isSaving
                ? 'bg-gray-400 text-gray-600 cursor-not-allowed'
                : 'bg-[#8DD3BB] text-white hover:bg-[#2e5245]'
            }`}
          >
            {isSaving ? 'Saving...' : 'Save Changes'}
          </motion.button>
        </div>

        {/* Save Status Indicator */}
        <AnimatePresence>
          {isSaving && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed bottom-4 right-4 bg-black bg-opacity-75 text-white px-4 py-2 rounded-md"
            >
              Saving changes...
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
    </div>
  );
};

export default Profil;