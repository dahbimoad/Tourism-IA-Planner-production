import axios from 'axios';

const API_URL = 'http://localhost:8000/';


export const getMessageFromAPI = async () => {
  try {
    const response = await axios.get(API_URL);
    return response.data.message;
  } catch (error) {
    console.error('Erreur lors de la récupération des données de l\'API :', error);
    throw error;
  }
};