import React, { useState, useEffect } from 'react';
import { FaWallet, FaCalendarDay, FaMapMarkerAlt } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import { usePreferences } from "../contexts/PreferencesContext";
import { TOURISM_IMAGES } from "../assets/tourismImages";


const Plans = () => {
  const { generatedPlans } = usePreferences();

  const [error, setError] = useState(false);
  const navigate = useNavigate();
  const [cachedImages, setCachedImages] = useState(() => {
    const saved = sessionStorage.getItem('planImages');
    return saved ? JSON.parse(saved) : {};
  });

  useEffect(() => {
    // Réinitialiser les images si le nombre de plans change
    const newImages = {};
    generatedPlans.forEach((_, index) => {
      newImages[index] = TOURISM_IMAGES[Math.floor(Math.random() * TOURISM_IMAGES.length)];
    });
    setCachedImages(newImages);
    sessionStorage.setItem('planImages', JSON.stringify(newImages));
  }, [generatedPlans]); // Déclenché à chaque changement de `generatedPlans`

  const getPlanTitle = (index) => {
    return `Plan ${index + 1}`;
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat("fr-MA", {
      style: "currency",
      currency: "MAD",
      minimumFractionDigits: 2,
    }).format(amount);
  };

  const renderCityDays = (plan) => {
    return plan.plan.map((city, index) => (
      <div key={index} className="flex justify-between items-center mb-2">
        <span className="text-gray-600">{city.city}:</span>
        <span className="flex items-center">
          <FaCalendarDay className="mr-1 text-[#8DD3BB]" />
          {city.days_spent} jour{city.days_spent > 1 ? 's' : ''}
        </span>
      </div>
    ));
  };

  return (
    <div className="min-h-screen bg-gray-100 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 py-16">
          Your Travel <span className="text-[#8DD3BB]">Plans</span> :
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {error ? (
            <div className="col-span-full text-center">
              <p className="text-red-500 mb-4">Error generating travel plans</p>
              <button
                onClick={() => setError(false)}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition duration-300"
              >
                Retry
              </button>
            </div>
          ) : generatedPlans.length > 0 ? (
            generatedPlans.map((plan, index) => (
              <div
                key={index}
                className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-2xl transition duration-300"
              >
                <img
                  src={cachedImages[index] || TOURISM_IMAGES[index % TOURISM_IMAGES.length]}
                  alt="Travel"
                  className="w-full h-48 object-cover"
                  onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = TOURISM_IMAGES[index % TOURISM_IMAGES.length];
                  }}
                />
                <div className="p-6">
                <h3 className="text-xl font-bold mb-2 flex items-center">
                <FaMapMarkerAlt className="mr-2 text-[#8DD3BB]" />
                 {getPlanTitle(index)}
               </h3>
                  
                  <p className="text-gray-600 mb-4">
                    <FaWallet className="inline mr-2" />
                    Total Cost: {formatCurrency(plan.total_cost)}
                  </p>

                  <div className="text-gray-600 mb-4">
                    <h4 className="font-semibold mb-2 flex items-center">
                      <FaCalendarDay className="mr-2 text-[#8DD3BB]" />
                      Jours par ville:
                    </h4>
                    {renderCityDays(plan)}
                  </div>

                  <button
                    onClick={() => navigate("/dashboard1/plan")}
                    className="w-full py-2 rounded-lg transition duration-300 bg-[#8DD3BB] hover:bg-[#7bc4a9]"
                  >
                    Details
                  </button>
                </div>
              </div>
            ))
          ) : (
            <div className="col-span-full text-center">
              <p className="text-gray-500">No travel plans generated yet</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Plans;