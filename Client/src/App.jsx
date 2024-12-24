import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import PrivateRoute from "./components/PrivateRoute";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import { AuthProvider } from './contexts/AuthContext';
import Dashboard from "./pages/Dashboard";


function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          {/* Utilisation de PrivateRoute pour protéger /dashboard */}
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                  <Dashboard />
              </PrivateRoute>
            }
          />
          {/* Ajoutez d'autres routes ici */}
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
