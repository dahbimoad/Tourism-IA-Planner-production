import { useState } from 'react';
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "./components/LoginPage";
import SignupPage from "./components/SignupPage";


function App() {
  return (
    <Router>
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignupPage />} />
      <Route path="/dashboard" element={<h1>Dashboard</h1>} />
      {/* Ajoutez d'autres routes ici */}
    </Routes>
  </Router>
  );
}

export default App;
