import React, { createContext, useState, useEffect } from 'react';
import { useCookies } from 'react-cookie';

const API_URL = import.meta.env.VITE_API_URL;

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [cookies, setCookie, removeCookie] = useCookies(['token']);
  const [token, setToken] = useState(cookies.token || '');
  const [user, setUser] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const login = async (credentials) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_URL}/user/signin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail?.message || 'Login failed');
      }

      if (data.access_token) {
        setToken(data.access_token);
        setCookie('token', data.access_token, { path: '/' });
        return true;
      }
      return false;
    } catch (error) {
      setError(error.message);
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  const handleGoogleLogin = async (response) => {
  setIsLoading(true);
  setError(null);
  try {
    console.log('Google response:', response); // Debug log

    const result = await fetch(`${API_URL}/auth/google`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        token: response.credential
      })
    });

    const data = await result.json();
    console.log('Backend response:', data); // Debug log

    if (!result.ok) {
      throw new Error(data.detail?.message || 'Backend request failed');
    }

    if (data.access_token) {
      setToken(data.access_token);
      setCookie('token', data.access_token, { path: '/' });
      return true;
    }
    return false;
  } catch (error) {
    console.error('Detailed Google login error:', error); // Debug log
    setError('Google login failed: ' + error.message);
    return false;
  } finally {
    setIsLoading(false);
  }
};

  const logout = () => {
    setToken('');
    setUser(null);
    removeCookie('token', { path: '/' });
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        login,
        logout,
        handleGoogleLogin,
        isAuthenticated: !!token,
        isLoading,
        error
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};