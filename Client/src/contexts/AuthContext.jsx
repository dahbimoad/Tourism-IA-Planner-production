import React, { createContext, useState, useEffect } from 'react';
import { useCookies } from 'react-cookie';

// Configuration des URLs
const API_URL = import.meta.env.VITE_API_URL;
const AUTH_ENDPOINTS = {
  signin: `${API_URL}${import.meta.env.VITE_AUTH_SIGNIN}`,
  signup: `${API_URL}${import.meta.env.VITE_AUTH_SIGNUP}`,
};

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [cookies, setCookie, removeCookie] = useCookies(['token']);
  const [token, setToken] = useState(cookies.token || '');
  const [user, setUser] = useState(null);

  useEffect(() => {
    if (token) {
      // Exemple : fetchUserInfo(token).then(...).catch(...)
      // setUser(...)
    } else {
      setUser(null);
    }
  }, [token]);

  const authenticate = async (url, payload) => {
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`Erreur: ${response.statusText}`);
      }

      const data = await response.json();
      const { access_token: tokenFromBackend, user: userFromBackend } = data;

      setToken(tokenFromBackend);
      setCookie('token', tokenFromBackend, { path: '/' });
      setUser(userFromBackend);

      return true;
    } catch (error) {
      console.error(error);
      return false;
    }
  };

  const login = (credentials) => {
    return authenticate(AUTH_ENDPOINTS.signin, credentials);
  };

  const signup = (userData) => {
    return authenticate(AUTH_ENDPOINTS.signup, userData);
  };

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