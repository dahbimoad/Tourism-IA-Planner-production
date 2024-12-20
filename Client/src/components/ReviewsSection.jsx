import React, { useState } from "react";
import { FaRoute, FaRegMoneyBillAlt, FaRegLightbulb, FaRegSmile, FaHeadset, FaHistory, FaPhone, FaEnvelope, FaFacebook, FaTwitter, FaInstagram, FaMapMarkerAlt, FaRobot } from "react-icons/fa";

const ReviewsSection = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    subject: "",
    message: ""
  });

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

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Form submitted:", formData);
  };

  return (
    <div className="w-full bg-white">
      <div className="container mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">WHAT OUR <span className="text-[#8DD3BB]">TRAVELERS</span> SAY</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <div key={index} className="bg-white p-6 rounded-lg shadow-lg">
              <div className="flex items-center mb-4">
                <img 
                  src={testimonial.image} 
                  alt={testimonial.name}
                  className="w-12 h-12 rounded-full object-cover mr-4"
                />
                <div>
                  <h3 className="font-semibold text-gray-800">{testimonial.name}</h3>
                  <p className="text-gray-600 text-sm">{testimonial.location}</p>
                </div>
              </div>
              <p className="text-gray-700 italic">"{testimonial.quote}"</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ReviewsSection;