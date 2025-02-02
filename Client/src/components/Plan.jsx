// Importation des dépendances nécessaires
import React, { useState, useContext, useEffect } from "react";
// Importation des icônes pour l'interface
import { FaPlane, FaHotel, FaMapMarkerAlt, FaCalendarAlt, FaWallet, FaClock, FaStar, FaTimes } from "react-icons/fa";
// Importation des composants pour l'indicateur de progression circulaire
import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";
// Importation des composants pour les animations
import { motion, AnimatePresence } from "framer-motion";
// Importation du contexte des préférences
import { PreferencesContext } from '../contexts/PreferencesContext';
// Importation des outils de gestion des paramètres d'URL
import { useSearchParams } from "react-router-dom";

const Plan = () => {
  // Récupération des préférences et des plans générés depuis le contexte
  const { preferences, generatedPlans } = useContext(PreferencesContext);
  // État pour gérer les paramètres de l'URL
  const [searchParams, setSearchParams] = useSearchParams();
  // État pour suivre le plan actuellement sélectionné
  const [selectedPlanIndex, setSelectedPlanIndex] = useState(0);
  // État pour gérer l'ouverture/fermeture de la modal d'édition
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);

  // Effet pour synchroniser l'index du plan avec l'URL
  useEffect(() => {
    const urlIndex = parseInt(searchParams.get('planIndex')) || 0;
    setSelectedPlanIndex(Math.min(urlIndex, generatedPlans.length - 1));
  }, [generatedPlans, searchParams]);

  // Effet pour mettre à jour l'URL quand l'index change
  useEffect(() => {
    setSearchParams({ planIndex: selectedPlanIndex }, { replace: true });
  }, [selectedPlanIndex, setSearchParams]);

  // Affichage d'un message si aucun plan n'est disponible
  if (!generatedPlans || generatedPlans.length === 0) {
    return (
      <div className="pt-24 text-center">
        <p>Aucun plan n'a été généré. Veuillez créer des préférences de voyage.</p>
      </div>
    );
  }

  // Récupération du plan actuel et des préférences actuelles
  const currentPlan = generatedPlans[selectedPlanIndex].plan;
  const currentPreference = preferences[preferences.length - 1];
  
  // Calcul des informations budgétaires
  const totalCost = generatedPlans[selectedPlanIndex].total_cost;
  const remainingBudget = currentPreference.budget - totalCost;
  const budgetScore = Math.round((totalCost / currentPreference.budget) * 100);

  // Fonction pour changer de plan
  const handlePlanChange = (index) => {
    if (index >= 0 && index < generatedPlans.length) {
      setSelectedPlanIndex(index);
    }
  };

  return (
    <div className="pt-24">
      <div className="relative">
        {/* Barre de navigation entre les différents plans */}
        <div className="flex justify-center mb-6 space-x-4">
          {generatedPlans.map((plan, index) => (
            <button
              key={index}
              onClick={() => handlePlanChange(index)}
              className={`px-4 py-2 rounded-lg ${
                selectedPlanIndex === index
                  ? "bg-blue-500 text-white"
                  : "bg-gray-200 text-gray-700"
              }`}
            >
              Plan {index + 1}
            </button>
          ))}
        </div>

        {/* Container principal avec animation */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="max-w-6xl mx-auto p-6 bg-white rounded-xl shadow-xl"
        >
          {/* En-tête avec ville de départ et indicateur de budget */}
          <motion.div className="flex flex-col md:flex-row justify-between items-center mb-8">
            <div className="space-y-2 w-full md:w-auto">
              <motion.div className="flex items-center space-x-4">
                <FaMapMarkerAlt className="text-[#8DD3BB] text-xl" />
                <div>
                  <h2 className="text-2xl font-bold text-gray-800">{currentPreference.lieuDepart}</h2>
                  <p className="text-sm text-gray-500">Departure City</p>
                </div>
              </motion.div>
            </div>

            {/* Indicateur circulaire d'utilisation du budget */}
            <motion.div className="mt-4 md:mt-0 w-32">
              <CircularProgressbar
                value={budgetScore}
                text={`${budgetScore}%`}
                styles={buildStyles({
                  textSize: "16px",
                  pathColor: `rgba(62, 152, 199, ${budgetScore / 100})`,
                  textColor: "#3e98c7",
                  trailColor: "#d6d6d6"
                })}
              />
              <p className="text-center mt-2 text-sm font-medium text-gray-600">Budget Usage</p>
            </motion.div>
          </motion.div>

          {/* Section aperçu du budget */}
          <div className="bg-blue-50 p-6 rounded-lg mb-8">
            <h3 className="text-xl font-semibold mb-4 flex items-center">
              <FaWallet className="mr-2 text-[#8DD3BB]" /> Budget Overview
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p className="text-gray-600">Total Budget</p>
                <p className="text-2xl font-bold text-gray-800">${currentPreference.budget}</p>
              </div>
              <div>
                <p className="text-gray-600">Remaining Budget</p>
                <p className="text-2xl font-bold text-green-600">${remainingBudget}</p>
              </div>
            </div>
          </div>

          {/* Liste des villes et activités prévues */}
          <div className="mb-8">
            <h3 className="text-xl font-semibold mb-4">Planned Cities & Activities</h3>
            <div className="space-y-4">
              {currentPlan.map((cityPlan, index) => (
                <div key={index} className="bg-gray-50 p-4 rounded-lg">
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="text-lg font-semibold text-gray-800">{cityPlan.city}</h4>
                    <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                      {cityPlan.days_spent} {cityPlan.days_spent > 1 ? 'days' : 'day'}
                    </span>
                  </div>
                  <p className="text-gray-600 mb-2">{cityPlan.hotel}</p>
                  <ul className="space-y-2">
                    {cityPlan.activities.map((activity, actIndex) => (
                      <li key={actIndex} className="flex items-center space-x-2">
                        <FaClock className="text-[#8DD3BB]" />
                        <span>{activity}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>

          {/* Section coût total estimé */}
          <div className="bg-gray-50 p-6 rounded-lg mb-8">
            <h3 className="text-xl font-semibold mb-4">Total Estimated Cost</h3>
            <div className="flex items-center space-x-3">
              <FaWallet className="text-[#8DD3BB]" />
              <div>
                <p className="text-gray-600">Total Cost</p>
                <p className="text-2xl font-bold">${totalCost}</p>
              </div>
            </div>
          </div>

          {/* Boutons d'action (Supprimer et Sauvegarder) */}
          <motion.div className="flex flex-col md:flex-row gap-4 justify-end">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-6 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
            >
              Delete
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
            >
              Save Plan
            </motion.button>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
};

export default Plan;