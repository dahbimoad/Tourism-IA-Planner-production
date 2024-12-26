import React, { useState } from "react";
import { FaPlane, FaMapMarkerAlt, FaCalendarAlt, FaWallet, FaCity } from "react-icons/fa";
import Select from "react-select";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const Plans = () => {
  const [selectedPlan, setSelectedPlan] = useState(null);
  const [error, setError] = useState(false);

  const sampleTravelPlans = [
    {
      id: 1,
      destination: "Plan 1",
      cost: "$3,500",
      image: "https://plus.unsplash.com/premium_photo-1673415819362-c2ca640bfafe?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
      itinerary: "Day 1-3: Sahara Exploration\nDay 4-6: Sahara Adventures"
    },
    {
      id: 2,
      destination: "Plan 2",
      cost: "$4,200",
      image: "https://plus.unsplash.com/premium_photo-1707242323176-3509a580f4d8?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
      itinerary: "Day 1-2: City Tour\nDay 3-4: Mt. Fuji Visit"
    },
    {
      id: 3,
      destination: "Plan 3",
      cost: "$5,000",
      image: "https://images.unsplash.com/photo-1531230689007-0b32d7a7c33e?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
      itinerary: "Day 1: Desert Safari\nDay 2-3: City Exploration"
    }
  ];

  


  return (
    <div className="min-h-screen bg-gray-100 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800  py-16">Your travel plans :</h1>
        {/* Travel Plans Display */}
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
          ) : (
            sampleTravelPlans.map((plan) => (
              <div
                key={plan.id}
                className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-2xl transition duration-300"
              >
                <img
                  src={plan.image}
                  alt={plan.destination}
                  className="w-full h-48 object-cover"
                  onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = "https://images.unsplash.com/photo-1488646953014-85cb44e25828";
                  }}
                />
                <div className="p-6">
                  <h3 className="text-xl font-bold mb-2">{plan.destination}</h3>
                  <p className="text-gray-600 mb-4">
                    <FaWallet className="inline mr-2" />
                    Estimated Cost: {plan.cost}
                  </p>
                  <p className="text-gray-600 mb-4 whitespace-pre-line">
                    <FaCity className="inline mr-2" />
                    {plan.itinerary}
                  </p>
                  <button
                    className="w-full py-2 rounded-lg transition duration-300 bg-[#8DD3BB]"
                  >
                    Details
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default Plans;