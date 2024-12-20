import { useState, useEffect } from "react";
import { FaRoute, FaPiggyBank, FaUserFriends } from "react-icons/fa";

const HeroSection = () => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  const features = [
    {
      icon: <FaRoute className="text-4xl text-[#8DD3BB]" />,
      title: "Personalized Itineraries",
      description: "Tailored travel plans just for you"
    },
    {
      icon: <FaPiggyBank className="text-4xl text-[#8DD3BB]" />,
      title: "Budget Optimization",
      description: "Maximum experience, minimum spending"
    },
    {
      icon: <FaUserFriends className="text-4xl text-[#8DD3BB]" />,
      title: "Local Insights",
      description: "Authentic Moroccan experiences"
    }
  ];

  return (
    <div className="relative min-h-full pt-6">
      <div
        className="absolute inset-0 z-0"
        style={{
          backgroundImage: "url('https://images.unsplash.com/photo-1539020140153-e479b8c22e70')",
          backgroundPosition: "center",
          backgroundSize: "cover",
          backgroundRepeat: "no-repeat"
        }}
      >
        <div className="absolute inset-0 bg-black/50" />
      </div>

      <div className="relative z-10 px-4 py-24 mx-auto max-w-7xl sm:px-6 lg:px-8">
        <div className={`text-center transition-all duration-1000 transform ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
          <h1 className="text-4xl font-extrabold tracking-tight text-white sm:text-5xl md:text-6xl">
            <span className="block">Revolutionize Your Travel</span>
            <span className="block text-[#8DD3BB]">Experience in Morocco!</span>
          </h1>

          <p className="max-w-2xl mx-auto mt-6 text-xl text-gray-200">
            Discover personalized itineraries crafted to your preferences, optimized for your budget, and enriched with authentic local experiences.
          </p>

          <div className="mt-10">
            <button
              className="px-8 py-4 text-lg font-medium text-white transition-all duration-300 transform bg-[#8DD3BB] rounded-full hover:bg-[#8DD3BB] hover:scale-105 focus:outline-none focus:ring-2 focus:ring-[#8DD3BB] focus:ring-offset-2"
              aria-label="Start Planning Your Adventure"
            >
              Start Planning Your Adventure
            </button>
          </div>
        </div>

        <div className="grid gap-8 mt-20 md:grid-cols-3">
          {features.map((feature, index) => (
            <div
              key={index}
              className={`p-6 text-center transition-all duration-1000 transform bg-white/10 backdrop-blur-md rounded-xl ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}
              style={{ transitionDelay: `${index * 200}ms` }}
            >
              <div className="flex justify-center">{feature.icon}</div>
              <h3 className="mt-4 text-xl font-semibold text-white">{feature.title}</h3>
              <p className="mt-2 text-gray-300">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default HeroSection;