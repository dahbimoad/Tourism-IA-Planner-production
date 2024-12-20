import React from "react";
import { FaRoute, FaRegMoneyBillAlt, FaRegLightbulb, FaRegSmile, FaHeadset, FaHistory } from "react-icons/fa";

const AboutSection = () => {
  const features = [
    {
      icon: <FaRoute className="text-4xl text-orange-600" />,
      title: "Personalized Itineraries",
      description: "Tailored travel plans that match your preferences and style"
    },
    {
      icon: <FaRegMoneyBillAlt className="text-4xl text-orange-600" />,
      title: "Budget Considerations",
      description: "Smart planning that optimizes your travel budget effectively"
    },
    {
      icon: <FaRegLightbulb className="text-4xl text-orange-600" />,
      title: "Local Insights",
      description: "Authentic recommendations from experienced local guides"
    },
    {
      icon: <FaRegSmile className="text-4xl text-orange-600" />,
      title: "User-friendly Interface",
      description: "Simple and intuitive platform for effortless planning"
    },
    {
      icon: <FaHeadset className="text-4xl text-orange-600" />,
      title: "24/7 Support",
      description: "Round-the-clock assistance for your travel needs"
    }
  ];

  const milestones = [
    {
      year: "2020",
      title: "Platform Launch",
      description: "Started our journey to revolutionize Morocco travel planning"
    },
    {
      year: "2021",
      title: "10,000+ Happy Travelers",
      description: "Reached milestone of serving thousands of adventurers"
    },
    {
      year: "2022",
      title: "Local Partnerships",
      description: "Established network with 100+ local guides and vendors"
    },
    {
      year: "2023",
      title: "Smart Planning",
      description: "Introduced AI-powered itinerary optimization"
    }
  ];

  const testimonials = [
    {
      name: "Sarah Thompson",
      location: "United States",
      quote: "The personalized itinerary made our Moroccan adventure truly unforgettable!",
      image: "https://images.unsplash.com/photo-1494790108377-be9c29b29330"
    },
    {
      name: "David Chen",
      location: "Singapore",
      quote: "Perfect balance of culture, adventure, and relaxation. Highly recommended!",
      image: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d"
    },
    {
      name: "Emma Martinez",
      location: "Spain",
      quote: "The local insights made our trip authentic and memorable.",
      image: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80"
    }
  ];

  return (
    <div className="w-full bg-white">
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