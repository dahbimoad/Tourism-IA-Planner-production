// Import de React et des outils de routage
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// Import des pages principales
import Home from "./pages/Home";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import UserInterface from "./pages/UserInterface";

// Import des composants
import PrivateRoute from "./components/PrivateRoute";
import Form from "./components/Form";
import Plans from "./components/Plans";
import Plan from "./components/Plan";
import FavouritesPlans from "./components/FavouritesPlans";

// Import des contextes pour la gestion d'état globale
import { AuthProvider } from './contexts/AuthContext';
import { PreferencesProvider  } from './contexts/PreferencesContext';

const App = () => {
  return (
    // AuthProvider: Gère l'état d'authentification dans toute l'application
    <AuthProvider>
      {/* PreferencesProvider: Gère les préférences utilisateur dans toute l'application */}
      <PreferencesProvider>
        {/* Router: Configure le routage de l'application */}
        <Router>
          {/* Routes: Contient toutes les routes de l'application */}
          <Routes>
            {/* Page d'accueil accessible à tous */}
            <Route path="/" element={<Home />} />
            
            {/* Routes pour l'authentification */}
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignupPage />} />

            {/* Dashboard protégé: nécessite une authentification */}
            <Route
              path="/dashboard"
              element={
                <PrivateRoute>
                  <UserInterface />
                </PrivateRoute>
              }
            >
              {/* Routes imbriquées dans le dashboard */}
              {/* Formulaire de préférences */}
              <Route path="form" element={<Form />} />
              {/* Liste des plans de voyage */}
              <Route path="plans" element={<Plans />} />
              {/* Détail d'un plan spécifique */}
              <Route path="plan" element={<Plan />} />
              {/* Plans favoris de l'utilisateur */}
              <Route path="FavouritesPlans" element={<FavouritesPlans />} />
            </Route>
          </Routes>
        </Router>
      </PreferencesProvider>
    </AuthProvider>
  );
};

export default App;