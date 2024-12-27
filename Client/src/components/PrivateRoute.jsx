import React, { useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import { Navigate } from 'react-router-dom';
import jwtDecode from 'jwt-decode';
 // Import correct

const PrivateRoute = ({ children }) => {
  const { token } = useContext(AuthContext);

  const isTokenValid = (token) => {
    try {
      // Décoder le token
      const decodedToken = jwtDecode(token);

      // Vérifier si la date d'expiration (exp) est toujours valide
      const currentTime = Date.now() / 1000; // Convertir en secondes
      return decodedToken.exp > currentTime;
    } catch (error) {
      // Si le décodage échoue, le token est invalide
      return false;
    }
  };

  if (!token || !isTokenValid(token)) {
    // Pas de token ou token invalide => redirection vers /login
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default PrivateRoute;
