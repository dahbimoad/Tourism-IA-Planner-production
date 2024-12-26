import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import PrivateRoute from "./components/PrivateRoute";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import { AuthProvider } from './contexts/AuthContext';
import Dashboard from "./pages/Dashboard";
import UserInterface from "./pages/UserInterface";

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/dashboard1" element={<UserInterface />} />
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          {/* Protecting /dashboard with PrivateRoute */}
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            }
          />
          {/* Add more routes here */}
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;
