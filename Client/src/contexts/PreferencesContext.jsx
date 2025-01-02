import React, { createContext, useContext } from 'react';
import { AuthContext } from './AuthContext';

const API_URL = import.meta.env.VITE_API_URL;

export const PreferencesContext = createContext();

export const PreferencesProvider = ({ children }) => {
  const { token } = useContext(AuthContext);

  const handleCreatePreference = async (preferenceData) => {
    try {
      const response = await fetch(`${API_URL}/preferences/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token && { 'Authorization': `Bearer ${token}` })
        },
        body: JSON.stringify({
          lieuDepart: preferenceData.lieuDepart,
          cities: preferenceData.cities,
          dateDepart: preferenceData.dateDepart,
          dateRetour: preferenceData.dateRetour,
          budget: parseFloat(preferenceData.budget)
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: 'Une erreur est survenue' }));
        throw new Error(errorData.message || `Erreur ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur dans handleCreatePreference:', error);
      throw new Error(error.message || 'Erreur lors de la création de la préférence');
    }
  };

  const getPreferences = async () => {
    try {
      const response = await fetch(`${API_URL}/preferences/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          ...(token && { 'Authorization': `Bearer ${token}` })
        }
      });

      if (!response.ok) {
        throw new Error(`Erreur ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur dans getPreferences:', error);
      throw error;
    }
  };

  return (
    <PreferencesContext.Provider 
      value={{ 
        handleCreatePreference,
        getPreferences
      }}
    >
      {children}
    </PreferencesContext.Provider>
  );
};

// Hook personnalisé
export const usePreferences = () => {
  const context = useContext(PreferencesContext);
  if (!context) {
    throw new Error('usePreferences doit être utilisé dans un PreferencesProvider');
  }
  return context;
};