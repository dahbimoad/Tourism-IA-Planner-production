import React, { useState } from "react";
import { FaHeart, FaTrash } from "react-icons/fa";
import { BsArrowRight } from "react-icons/bs";
import { motion } from "framer-motion";
import "react-circular-progressbar/dist/styles.css";
import { useNavigate } from "react-router-dom";


const FavouritesPlans = () => {
  const navigate = useNavigate();
  const [favoritePlans, setFavoritePlans] = useState([
    {
      id: 1,
      name: "Paradise Beach Getaway",
      image: "https://images.unsplash.com/photo-1506929562872-bb421503ef21",
      dates: "Aug 15 - Aug 25, 2024",
      budget: "$2,500",
      location: "Maldives"
    },
    {
      id: 2,
      name: "Mountain Adventure",
      image: "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b",
      dates: "Sep 10 - Sep 20, 2024",
      budget: "$3,200",
      location: "Swiss Alps"
    },
    {
      id: 3,
      name: "Cultural City Tour",
      image: "https://images.unsplash.com/photo-1522083165195-3424ed129620",
      dates: "Oct 5 - Oct 15, 2024",
      budget: "$4,000",
      location: "Paris"
    }
  ]);

  const removePlan = (id) => {
    setFavoritePlans(favoritePlans.filter((plan) => plan.id !== id));
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1
    }
  };

  return (
    <div className="pt-16">
        <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8"
    >
      <div className="max-w-7xl mx-auto">
        <motion.div 
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold text-gray-900 mb-4 text-start">
            Your Favorite <span className="text-[#8DD3BB]">Travel</span> Plans
          </h1>
          <p className="text-lg text-gray-600 text-start">
            Manage and explore your dream destinations
          </p>
        </motion.div>

        {favoritePlans.length === 0 ? (
          <motion.div 
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.5 }}
            className="text-center py-16 bg-white rounded-lg shadow-md"
          >
            <FaHeart className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h2 className="text-2xl font-semibold text-gray-600 mb-2">
              No Favorites Yet
            </h2>
            <p className="text-gray-500">
              Start adding your dream destinations to favorites!
            </p>
          </motion.div>
        ) : (
          <motion.div 
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
          >
            {favoritePlans.map((plan) => (
              <motion.div
                key={plan.id}
                variants={itemVariants}
                whileHover={{ scale: 1.03 }}
                className="bg-white rounded-xl shadow-lg overflow-hidden"
              >
                <div className="relative">
                  <img
                    src={plan.image}
                    alt={plan.name}
                    className="w-full h-48 object-cover"
                    onError={(e) => {
                      e.target.src = "https://images.unsplash.com/photo-1436491865332-7a61a109cc05";
                    }}
                  />
                  <motion.button
                    onClick={() => removePlan(plan.id)}
                    whileHover={{ scale: 1.1, backgroundColor: "#EF4444" }}
                    whileTap={{ scale: 0.95 }}
                    className="absolute top-4 right-4 p-2 rounded-full bg-white shadow-md hover:text-white transition-colors duration-300"
                  >
                    <FaTrash className="w-4 h-4" />
                  </motion.button>
                </div>

                <div className="p-6">
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    {plan.name}
                  </h3>
                  <div className="space-y-2 mb-4">
                    <p className="text-gray-600">
                      <span className="font-medium">Location:</span>{" "}
                      {plan.location}
                    </p>
                    <p className="text-gray-600">
                      <span className="font-medium">Dates:</span> {plan.dates}
                    </p>
                    <p className="text-gray-600">
                      <span className="font-medium">Budget:</span> {plan.budget}
                    </p>
                  </div>

                  <motion.button onClick={() => navigate("/dashboard1/plan")}
                    whileHover={{ scale: 1.01 }}
                    whileTap={{ scale: 0.98 }}
                    className="w-full bg-[#8DD3BB] text-white py-2 px-4 rounded-lg hover:bg-green-700 transition-colors duration-300 flex items-center justify-center space-x-2"
                  >
                    <button >View Details</button>
                    <BsArrowRight className="w-4 h-4" />
                  </motion.button>
                </div>
              </motion.div>
            ))}
          </motion.div>
        )}
      </div>
    </motion.div>
    </div>
  );
};

export default FavouritesPlans;