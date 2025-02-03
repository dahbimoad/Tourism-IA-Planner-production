import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import PrivateRoute from "./components/PrivateRoute";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import { AuthProvider } from './contexts/AuthContext';
import { ProfileProvider } from './contexts/ProfileContext'; // Add ProfileProvider
import { PreferencesProvider } from './contexts/PreferencesContext';
import UserInterface from "./pages/UserInterface";
import Form from "./components/Form";
import Plans from "./components/Plans";
import Profil from "./components/Profil";
import Plan from "./components/Plan";
import FavouritesPlans from "./components/FavouritesPlans";

const App = () => {
  return (
    <AuthProvider>
      <ProfileProvider> {/* Add ProfileProvider here */}
        <PreferencesProvider>
          <Router>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/signup" element={<SignupPage />} />

              <Route
                path="/dashboard1"
                element={
                  <PrivateRoute>
                    <UserInterface />
                  </PrivateRoute>
                }
              >
                <Route path="form" element={<Form />} />
                <Route path="plans" element={<Plans />} />
                <Route path="plan" element={<Plan />} />
                <Route path="profil" element={<Profil />} />
                <Route path="FavouritesPlans" element={<FavouritesPlans />} />
              </Route>
            </Routes>
          </Router>
        </PreferencesProvider>
      </ProfileProvider> {/* Close ProfileProvider here */}
    </AuthProvider>
  );
};

export default App;