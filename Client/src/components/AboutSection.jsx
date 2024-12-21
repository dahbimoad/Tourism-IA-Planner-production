import React from "react";
import { FaRoute, FaRegMoneyBillAlt, FaRegLightbulb, FaRegSmile, FaHeadset, FaHistory } from "react-icons/fa";

const AboutSection = () => {
  return (
    <div className="w-full bg-white" id="about">
      <div className="container mx-auto px-4 py-16">
      <h2 className="text-4xl font-bold mb-6 text-gray-800 text-center pb-8">ABOUT <span className="text-[#8DD3BB]">US</span></h2> 
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            
          <div>
            
            <img 
              src="https://images.unsplash.com/photo-1730581822475-95e793915e4e?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" 
              alt="Moroccan Landmark"
              className="rounded-lg shadow-xl w-full h-[400px] object-cover"
            />
          </div>
          <div>
            <h2 className="text-3xl font-bold mb-6 text-gray-800">Welcome to Smart Morocco Travel</h2>
            <p className="text-lg text-gray-600 mb-8">
              Our innovative platform revolutionizes travel planning in Morocco by creating personalized itineraries that match your preferences, budget, and travel style. We combine cutting-edge technology with local expertise to ensure every journey is unique and memorable.
            </p>
          </div>
        </div>
      </div>

      

      

      

      
    </div>
  );
};

export default AboutSection;