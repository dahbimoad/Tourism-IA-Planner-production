import React, { useState, useEffect } from "react";
import ChatInterface from "./ChatInterface";
import { 
  FaFacebookF, 
  FaInstagram, 
  FaTwitter, 
  FaLinkedinIn, 
  FaMapMarkerAlt, 
  FaEnvelope, 
  FaPhone, 
  FaArrowUp, 
  FaHome, 
  FaInfoCircle, 
  FaRoute, 
  FaBlog, 
  FaAddressBook, 
  FaCommentDots 
} from "react-icons/fa";

const Footer = () => {
  const [showScrollButton, setShowScrollButton] = useState(false);
  const [moroccoTime, setMoroccoTime] = useState("");
  const [fontSize, setFontSize] = useState("normal");
  const [showChat, setShowChat] = useState(false);

  const quotes = [
    "Travel is the only thing you buy that makes you richer",
    "Adventure awaits in every corner of Morocco",
    "Life is either a daring adventure or nothing at all",
    "Traveling – it leaves you speechless, then turns you into a storyteller"
  ];

  const [currentQuote, setCurrentQuote] = useState(quotes[0]);

  useEffect(() => {
    const handleScroll = () => {
      setShowScrollButton(window.scrollY > 300);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  useEffect(() => {
    const updateMoroccoTime = () => {
      const time = new Date().toLocaleTimeString("en-US", {
        timeZone: "Africa/Casablanca",
        hour12: true,
      });
      setMoroccoTime(time);
    };

    updateMoroccoTime();
    const interval = setInterval(updateMoroccoTime, 1000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
      setCurrentQuote(randomQuote);
    }, 24000);

    return () => clearInterval(interval);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const toggleFontSize = () => {
    setFontSize(prev => prev === "normal" ? "large" : "normal");
  };

  return (
    <footer className="bg-[#8DD3BB] text-white pt-12 relative">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* About Us Section */}
          <div className="space-y-4">
            <h3 className="text-2xl font-semibold text-gray-800">About Us</h3>
            <p className="text-gray-100">Revolutionizing Moroccan travel one journey at a time.</p>
            <div className="h-1 w-20 bg-gray-800 rounded"></div>
          </div>

          {/* Quick Links */}
          <div className="space-y-4">
            <h3 className="text-2xl font-semibold text-gray-800">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <a href="#" className="flex items-center space-x-2 hover:text-gray-500 transition-colors">
                  <FaHome className="text-gray-800" />
                  <span>Home</span>
                </a>
              </li>
              <li>
                <a href="#" className="flex items-center space-x-2 hover:text-gray-500 transition-colors">
                  <FaInfoCircle className="text-gray-800" />
                  <span>About</span>
                </a>
              </li>
              <li>
                <a href="#" className="flex items-center space-x-2 hover:text-gray-500 transition-colors">
                  <FaRoute className="text-gray-800" />
                  <span>Itineraries</span>
                </a>
              </li>
              <li>
                <a href="#" className="flex items-center space-x-2 hover:text-gray-500 transition-colors">
                  <FaBlog className="text-gray-800" />
                  <span>Blog</span>
                </a>
              </li>
              <li>
                <a href="#" className="flex items-center space-x-2 hover:text-gray-500 transition-colors">
                  <FaAddressBook className="text-gray-800" />
                  <span>Contact</span>
                </a>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div className="space-y-4">
            <h3 className="text-2xl font-semibold text-gray-800">Contact Us</h3>
            <div className="space-y-2">
              <p className="flex items-center space-x-2">
                <FaEnvelope className="text-gray-800" />
                <span>contact@moroccotravel.com</span>
              </p>
              <p className="flex items-center space-x-2">
                <FaPhone className="text-gray-800" />
                <span>+212 123 456 789</span>
              </p>
              <p className="flex items-center space-x-2">
                <FaMapMarkerAlt className="text-gray-800" />
                <span>Based in Morocco, serving travelers worldwide</span>
              </p>
            </div>
          </div>

          {/* Newsletter Signup */}
          <div className="space-y-4">
            <h3 className="text-2xl font-semibold text-gray-800">Newsletter</h3>
            <div className="space-y-2">
              <input
                type="email"
                placeholder="Enter your email for travel updates"
                className="w-full px-4 py-2 bg-gray-800 rounded focus:outline-none focus:ring-2 focus:ring-gray-500"
              />
              <button className="w-full px-4 py-2 bg-gray-800 rounded hover:bg-gray-600 transition-colors">
                Subscribe
              </button>
            </div>
          </div>
        </div>

        {/* Social Media Icons */}
        <div className="flex justify-center space-x-6 mt-8 pb-8">
          <a href="#" className="text-2xl hover:text-blue-500 transition-transform hover:scale-110">
            <FaFacebookF />
          </a>
          <a href="#" className="text-2xl hover:text-red-300 transition-transform hover:scale-110">
            <FaInstagram />
          </a>
          <a href="#" className="text-2xl hover:text-blue-400 transition-transform hover:scale-110">
            <FaLinkedinIn />
          </a>
        </div>

        {/* Dynamic Quote and Time */}
        <div className="text-center py-4 border-t border-[#6ac1a2]">
          <p className="text-gray-900">{currentQuote}</p>
          <p className="text-gray-800 bold mt-2">Morocco Time: {moroccoTime}</p>
        </div>

        {/* Copyright */}
        <div className="text-center py-4 border-t border-[#6ac1a2]">
          <p className="text-gray-900">&copy; {new Date().getFullYear()} Morocco Travel. All rights reserved.</p>
        </div>
      </div>

      {/* Chatbot Button */}
      <button
        onClick={() => setShowChat(!showChat)}
        className="fixed bottom-8 left-8 bg-gray-800 p-4 rounded-full hover:bg-[#8DD3BB] transition-colors z-50 shadow-lg"
        aria-label="Open chat"
      >
        <FaCommentDots className="text-xl text-white" />
        {!showChat && (
          <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full text-xs text-white flex items-center justify-center">
            !
          </span>
        )}
      </button>

      {/* Chat Interface */}
      {showChat && <ChatInterface onClose={() => setShowChat(false)} />}
    {/* ... rest of the footer ... */}
      {/* Scroll to Top Button */}
      {showScrollButton && (
        <button
          onClick={scrollToTop}
          className="fixed bottom-8 right-8 bg-gray-800 p-3 rounded-full hover:bg-[#8DD3BB] transition-colors z-50"
          aria-label="Scroll to top"
        >
          <FaArrowUp className="text-white" />
        </button>
      )}

      {/* Add your Chat component here */}
      {/* {showChat && <ChatComponent />} */}
    </footer>
  );
};

export default Footer;