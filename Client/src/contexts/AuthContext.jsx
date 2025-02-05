import React, { createContext, useState, useEffect, useCallback } from 'react';
import { useCookies } from 'react-cookie';
import { googleLogout } from '@react-oauth/google';

const API_URL = import.meta.env.VITE_API_URL;

const AUTH_ENDPOINTS = {
  signin: `${API_URL}${import.meta.env.VITE_AUTH_SIGNIN}`,
  signup: `${API_URL}${import.meta.env.VITE_AUTH_SIGNUP}`,
  google: `${API_URL}/auth/google`,
};

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [cookies, setCookie, removeCookie] = useCookies(['token']);
  const [token, setToken] = useState(cookies.token || '');
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Initialisation Google OAuth
  useEffect(() => {
    const initGoogleAuth = () => {
      try {
        window.google.accounts.id.initialize({
          client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
          callback: handleGoogleResponse,
          auto_select: false,
        });
        
        window.google.accounts.id.renderButton(
          document.getElementById('googleSignInButton'),
          { theme: 'filled_blue', size: 'medium' }
        );
      } catch (err) {
        console.error('Erreur initialisation Google Auth:', err);
      }
    };

    if (window.google) {
      initGoogleAuth();
    }
  }, []);

  // Gestion réponse Google
  const handleGoogleResponse = useCallback(async (response) => {
    try {
      setIsLoading(true);
      const res = await fetch(AUTH_ENDPOINTS.google, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ credential: response.credential }),
      });

      const data = await res.json();
      
      if (!res.ok) throw new Error(data.message || 'Google authentication failed');

      setToken(data.access_token);
      setCookie('token', data.access_token, { 
        path: '/', 
        secure: true, 
        sameSite: 'strict' 
      });
      setUser(data.user);
      
    } catch (err) {
      setError(err.message);
      googleLogout();
    } finally {
      setIsLoading(false);
    }
  }, [setCookie]);

  // Authentification standard
  const authenticate = async (url, payload) => {
    try {
      setIsLoading(true);
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.message);

      setToken(data.access_token);
      setCookie('token', data.access_token, { 
        path: '/', 
        secure: true, 
        sameSite: 'strict' 
      });
      setUser(data.user);

    } catch (err) {
      setError(err.message);
      return false;
    } finally {
      setIsLoading(false);
    }
    return true;
  };

  const login = (credentials) => authenticate(AUTH_ENDPOINTS.signin, credentials);
  const signup = (userData) => authenticate(AUTH_ENDPOINTS.signup, userData);

  const logout = () => {
    setToken('');
    removeCookie('token');
    setUser(null);
    googleLogout();
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        login,
        signup,
        logout,
        isLoading,
        error,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};