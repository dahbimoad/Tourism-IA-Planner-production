import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import PrivateRoute from "./components/PrivateRoute";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import { AuthProvider } from './contexts/AuthContext';
import Dashboard from "./pages/Dashboard";
import UserInterface from "./pages/UserInterface";
import Form from "./components/Form";
import Plans from "./components/Plans";
import Plan from "./components/Plan";
import FavouritesPlans from "./components/FavouritesPlans";

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
          <Route path="/dashboard1" element={<UserInterface />}>
            <Route path="form" element={<Form />} />
            <Route path="plans" element={<Plans />} />
            <Route path="plan" element={<Plan />} />
            <Route path="FavouritesPlans" element={<FavouritesPlans />} />
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;
