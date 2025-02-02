import React, { createContext, useContext, useState } from 'react';
import axios from 'axios';
import { AuthContext } from './AuthContext';

const API_URL = import.meta.env.VITE_API_URL;

export const PreferencesContext = createContext();

export const PreferencesProvider = ({ children }) => {
  const { token } = useContext(AuthContext);
  const [preferences, setPreferences] = useState([]);
  const [generatedPlans, setGeneratedPlans] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

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
      setPreferences(prev => [...prev, data.preference]);
      setGeneratedPlans(data.generated_plans);
      
      return data;
    } catch (error) {
      let errorMessage = 'Une erreur est survenue';
      
      if (error.response) {
        // Erreur de réponse du serveur
        const errorData = error.response.data;
        errorMessage = errorData.message || `Erreur ${error.response.status}`;
      } else if (error.request) {
        // Requête effectuée mais pas de réponse
        errorMessage = 'Pas de réponse du serveur';
      } else {
        // Erreur de configuration de la requête
        errorMessage = error.message;
      }

      console.error('Erreur lors de la création de la préférence:', error);
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <PreferencesContext.Provider 
      value={{ 
        handleCreatePreference,
        preferences,
        generatedPlans,
        isLoading,
        error
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