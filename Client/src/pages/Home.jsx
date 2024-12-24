import React, { useEffect, useState } from 'react';
import { getMessageFromAPI } from '../services/api';
import MessageDisplay from '../components/MessageDisplay';
import Navbar from '../components/Navbar';
import './Home.css';

const Home = () => {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const apiMessage = await getMessageFromAPI();
        setMessage(apiMessage);
      } catch (error) {
        setMessage('Erreur lors de la récupération du message.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="home-container">
      <Navbar />
      <h1>Bienvenue sur la page d'accueil</h1>
      {loading ? (
        <p>Chargement...</p>
      ) : (
        <MessageDisplay message={message} />
      )}
    </div>
  );
};

export default Home;
