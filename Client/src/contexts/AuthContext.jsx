// AuthContext.jsx
import React, { createContext, useState, useEffect } from 'react';
import { useCookies } from 'react-cookie';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [cookies, setCookie, removeCookie] = useCookies(['token']);
  
  // On initialise le token depuis le cookie si présent
  const [token, setToken] = useState(cookies.token || '');
  const [user, setUser] = useState(null);

  /**
   * useEffect : si le token change, on peut aller récupérer
   * les infos utilisateur (ou bien on les récupère déjà lors du login/signup).
   */
  useEffect(() => {
    if (token) {
      // Exemple : fetchUserInfo(token).then(...).catch(...)
      // setUser(...)
    } else {
      setUser(null);
    }
  }, [token]);

  
  /**
   * Petite fonction utilitaire pour éviter la duplication de code
   * lors des appels d'authentification (login/signup).
   */
  const authenticate = async (url, payload) => {
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        // Gère les cas d’erreur : par ex. 400, 401, etc.
        throw new Error(`Erreur: ${response.statusText}`);
      }

      // On suppose que la réponse renvoie { token, user }
      const data = await response.json();
      const { access_token: tokenFromBackend, user: userFromBackend } = data;

      // Mettre à jour le state et le cookie
      setToken(tokenFromBackend);
      setCookie('token', tokenFromBackend, { path: '/' });
      setUser(userFromBackend);

      return true;
    } catch (error) {
      console.error(error);
      return false;
    }
  };

  /**
   * login(credentials)
   * Exemple de credentials : { email: '...', password: '...' }
   */
  const login = (credentials) => {
    return authenticate('https://tourism-ia-planner-production-client.onrender.com/user/signin', credentials);
  };

  /**
   * signup(userData)
   * Exemple de userData :
   * {
   *   "nom": "Doe",
   *   "prenom": "John",
   *   "email": "john.doe@example.com",
   *   "password": "securepassword123"
   * }
   */
  const signup = (userData) => {
    return authenticate('https://tourism-ia-planner-production-client.onrender.com/user/signup', userData);
  };

  /**
   * logout()
   * On réinitialise tout côté client
   */
  const logout = () => {
    setToken('');
    removeCookie('token', { path: '/' });
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        login,
        signup,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
