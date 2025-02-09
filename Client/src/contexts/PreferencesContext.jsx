import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import { AuthContext } from './AuthContext';

const API_URL = import.meta.env.VITE_API_URL;

export const PreferencesContext = createContext();

const STORAGE_KEYS = {
  PREFERENCES: 'userPreferences',
  GENERATED_PLANS: 'generatedPlans'
};

export const PreferencesProvider = ({ children }) => {
  const { token } = useContext(AuthContext);
  
  const [preferences, setPreferences] = useState(() => {
    const savedPreferences = localStorage.getItem(STORAGE_KEYS.PREFERENCES);
    return savedPreferences ? JSON.parse(savedPreferences) : [];
  });

  const [generatedPlans, setGeneratedPlans] = useState(() => {
    const savedPlans = localStorage.getItem(STORAGE_KEYS.GENERATED_PLANS);
    return savedPlans ? JSON.parse(savedPlans) : [];
  });

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEYS.PREFERENCES, JSON.stringify(preferences));
  }, [preferences]);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEYS.GENERATED_PLANS, JSON.stringify(generatedPlans));
  }, [generatedPlans]);

  const handleCreatePreference = async (preferenceData) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await axios.post(
        `${API_URL}/preferences/`,
        {
          lieuDepart: preferenceData.lieuDepart,
          cities: preferenceData.cities,
          dateDepart: preferenceData.dateDepart,
          dateRetour: preferenceData.dateRetour,
          budget: parseFloat(preferenceData.budget)
        },
        {
          headers: {
            'Content-Type': 'application/json',
            ...(token && { Authorization: `Bearer ${token}` })
          }
        }
      );

      const data = response.data;
      
      // Vider le localStorage avant de mettre à jour avec les nouvelles données
      localStorage.removeItem(STORAGE_KEYS.PREFERENCES);
      localStorage.removeItem(STORAGE_KEYS.GENERATED_PLANS);
      
      // Mettre à jour les états avec uniquement les nouvelles données
      setPreferences([data.preference]);
      setGeneratedPlans(data.generated_plans);
      
      return data;
    } catch (error) {
      let errorMessage = 'Une erreur est survenue';
      
      if (error.response) {
        const errorData = error.response.data;
        errorMessage = errorData.message || `Erreur ${error.response.status}`;
      } else if (error.request) {
        errorMessage = 'Pas de réponse du serveur';
      } else {
        errorMessage = error.message;
      }

      console.error('Erreur lors de la création de la préférence:', error);
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const clearStoredData = () => {
    localStorage.removeItem(STORAGE_KEYS.PREFERENCES);
    localStorage.removeItem(STORAGE_KEYS.GENERATED_PLANS);
    setPreferences([]);
    setGeneratedPlans([]);
  };

  return (
    <PreferencesContext.Provider 
      value={{ 
        handleCreatePreference,
        preferences,
        generatedPlans,
        isLoading,
        error,
        clearStoredData
      }}
    >
      {children}
    </PreferencesContext.Provider>
  );
};

export const usePreferences = () => {
  const context = useContext(PreferencesContext);
  if (!context) {
    throw new Error('usePreferences doit être utilisé dans un PreferencesProvider');
  }
  return context;
};