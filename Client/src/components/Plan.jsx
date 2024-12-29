import React, { useState } from "react";
import { FaPlane, FaHotel, FaMapMarkerAlt, FaCalendarAlt, FaWallet, FaClock, FaStar, FaTimes } from "react-icons/fa";
import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";
import { motion, AnimatePresence } from "framer-motion";

const Plan = () => {
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [travelPlan, setTravelPlan] = useState({
    departure: "Tanger",
    destination: "Marrakech",
    departureDate: "2024-06-15",
    returnDate: "2024-06-25",
    totalBudget: 5000,
    remainingBudget: 3200,
    activities: [
      { id: 1, name: "Eiffel Tower Visit", cost: 25 },
      { id: 2, name: "Seine River Cruise", cost: 45 },
      { id: 3, name: "Louvre Museum Tour", cost: 65 },
      { id: 4, name: "Palace of Versailles", cost: 85 }
    ],
    costs: {
      flight: 800,
      hotel: 1200,
      activities: 220
    },
    score: 85
  });

  const [editFormData, setEditFormData] = useState({ ...travelPlan });

  const handleEdit = () => {
    setIsEditModalOpen(true);
    setEditFormData({ ...travelPlan });
  };

  const handleSave = () => {
    setTravelPlan(editFormData);
    setIsEditModalOpen(false);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setEditFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleCostChange = (type, value) => {
    setEditFormData(prev => ({
      ...prev,
      costs: {
        ...prev.costs,
        [type]: parseInt(value) || 0
      }
    }));
  };

  const generateNewPlan = () => {
    console.log("Generating new plan");
  };

  return (
    <div className="pt-24">
        <div className="relative">
      <AnimatePresence>
        {isEditModalOpen && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.8, opacity: 0 }}
              className="bg-white rounded-xl p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto"
            >
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-800">Edit Travel Plan</h2>
                <button
                  onClick={() => setIsEditModalOpen(false)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  <FaTimes size={24} />
                </button>
              </div>

              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Departure City</label>
                    <input
                      type="text"
                      name="departure"
                      value={editFormData.departure}
                      onChange={handleInputChange}
                      className="w-full p-2 border rounded-lg"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Destination City</label>
                    <input
                      type="text"
                      name="destination"
                      value={editFormData.destination}
                      onChange={handleInputChange}
                      className="w-full p-2 border rounded-lg"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Departure Date</label>
                    <input
                      type="date"
                      name="departureDate"
                      value={editFormData.departureDate}
                      onChange={handleInputChange}
                      className="w-full p-2 border rounded-lg"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Return Date</label>
                    <input
                      type="date"
                      name="returnDate"
                      value={editFormData.returnDate}
                      onChange={handleInputChange}
                      className="w-full p-2 border rounded-lg"
                    />
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-2">Costs</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Flight Cost</label>
                      <input
                        type="number"
                        value={editFormData.costs.flight}
                        onChange={(e) => handleCostChange("flight", e.target.value)}
                        className="w-full p-2 border rounded-lg"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Hotel Cost</label>
                      <input
                        type="number"
                        value={editFormData.costs.hotel}
                        onChange={(e) => handleCostChange("hotel", e.target.value)}
                        className="w-full p-2 border rounded-lg"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Activities Cost</label>
                      <input
                        type="number"
                        value={editFormData.costs.activities}
                        onChange={(e) => handleCostChange("activities", e.target.value)}
                        className="w-full p-2 border rounded-lg"
                      />
                    </div>
                  </div>
                </div>

                <div className="flex justify-end space-x-4 mt-6">
                  <button
                    onClick={() => setIsEditModalOpen(false)}
                    className="px-4 py-2 text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleSave}
                    className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
                  >
                    Save Changes
                  </button>
                </div>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="max-w-6xl mx-auto p-6 bg-white rounded-xl shadow-xl"
      >
        {/* Rest of your existing code */}
        {/* Header Section */}
        <motion.div 
          initial={{ x: -20 }}
          animate={{ x: 0 }}
          transition={{ delay: 0.2 }}
          className="flex flex-col md:flex-row justify-between items-center mb-8"
        >
          <div className="space-y-2 w-full md:w-auto">
            <motion.div 
              whileHover={{ scale: 1.05 }}
              className="flex items-center space-x-4"
            >
              <FaMapMarkerAlt className="text-[#8DD3BB] text-xl" />
              <div>
                <h2 className="text-2xl font-bold text-gray-800">{travelPlan.departure}</h2>
                <p className="text-sm text-gray-500">Departure City</p>
              </div>
            </motion.div>
            <motion.div 
              whileHover={{ scale: 1.05 }}
              className="flex items-center space-x-4"
            >
              <FaPlane className="text-[#8DD3BB] text-xl" />
              <div>
                <h2 className="text-2xl font-bold text-gray-800">{travelPlan.destination}</h2>
                <p className="text-sm text-gray-500">Destination City</p>
              </div>
            </motion.div>
          </div>

          <motion.div 
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.4 }}
            className="mt-4 md:mt-0 w-32"
          >
            <CircularProgressbar
              value={travelPlan.score}
              text={`${travelPlan.score}%`}
              styles={buildStyles({
                textSize: "16px",
                pathColor: `rgba(62, 152, 199, ${travelPlan.score / 100})`,
                textColor: "#3e98c7",
                trailColor: "#d6d6d6"
              })}
            />
            <p className="text-center mt-2 text-sm font-medium text-gray-600">Travel Score</p>
          </motion.div>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="flex items-center space-x-3">
              <FaCalendarAlt className="text-[#8DD3BB]" />
              <div>
                <p className="text-sm text-gray-500">Departure Date</p>
                <p className="font-semibold">{new Date(travelPlan.departureDate).toLocaleDateString()}</p>
              </div>
            </div>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="flex items-center space-x-3">
              <FaCalendarAlt className="text-[#8DD3BB]" />
              <div>
                <p className="text-sm text-gray-500">Return Date</p>
                <p className="font-semibold">{new Date(travelPlan.returnDate).toLocaleDateString()}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-blue-50 p-6 rounded-lg mb-8">
          <h3 className="text-xl font-semibold mb-4 flex items-center">
            <FaWallet className="mr-2 text-[#8DD3BB]" /> Budget Overview
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="text-gray-600">Total Budget</p>
              <p className="text-2xl font-bold text-gray-800">${travelPlan.totalBudget}</p>
            </div>
            <div>
              <p className="text-gray-600">Remaining Budget</p>
              <p className="text-2xl font-bold text-green-600">${travelPlan.remainingBudget}</p>
            </div>
          </div>
        </div>

        <div className="mb-8">
          <h3 className="text-xl font-semibold mb-4">Planned Activities</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {travelPlan.activities.map((activity) => (
              <div key={activity.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <FaClock className="text-[#8DD3BB]" />
                  <span>{activity.name}</span>
                </div>
                <span className="font-semibold">${activity.cost}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-gray-50 p-6 rounded-lg mb-8">
          <h3 className="text-xl font-semibold mb-4">Estimated Costs</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="flex items-center space-x-3">
              <FaPlane className="text-[#8DD3BB]" />
              <div>
                <p className="text-gray-600">Flight</p>
                <p className="text-xl font-bold">${travelPlan.costs.flight}</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <FaHotel className="text-[#8DD3BB]" />
              <div>
                <p className="text-gray-600">Hotel</p>
                <p className="text-xl font-bold">${travelPlan.costs.hotel}</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <FaStar className="text-[#8DD3BB]" />
              <div>
                <p className="text-gray-600">Activities</p>
                <p className="text-xl font-bold">${travelPlan.costs.activities}</p>
              </div>
            </div>
          </div>
        </div>

        <motion.div 
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="flex flex-col md:flex-row gap-4 justify-end"
        >
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleEdit}
            className="px-6 py-2 bg-red-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
          >
            Delete
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleEdit}
            className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
          >
            Edit Plan
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={generateNewPlan}
            className="px-6 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors"
          >
            Generate New Plan
          </motion.button>
        </motion.div>
      </motion.div>
    </div>

    </div>
  );
};

export default Plan;