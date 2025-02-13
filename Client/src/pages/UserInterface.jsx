import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import NavbarUser from '../components/NavbarUser';
import ChatInterface from "../components/ChatInterface";
import { FaArrowUp } from "react-icons/fa";
import { MessageCircle } from 'lucide-react';

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
};

const UserInterface = () => {
  const [showChat, setShowChat] = useState(false);
  const [showScrollButton, setShowScrollButton] = useState(false);

  return (
    <div>
      <NavbarUser />
      <div>
        <Outlet />
      </div>
      
      {/* Chat Button - moved to left side */}
      <button
        onClick={() => setShowChat(true)}
        className="fixed bottom-8 left-8 bg-[#8DD3BB] p-4 rounded-full hover:bg-gray-800 transition-colors z-50"
        aria-label="Open chat"
      >
        <MessageCircle className="text-white" size={24} />
      </button>

      {/* Chat Interface */}
      {showChat && <ChatInterface onClose={() => setShowChat(false)} />}

      {/* Scroll to Top Button */}
      {showScrollButton && (
        <button
          onClick={scrollToTop}
          className="fixed bottom-24 right-8 bg-gray-800 p-3 rounded-full hover:bg-[#8DD3BB] transition-colors z-50"
          aria-label="Scroll to top"
        >
          <FaArrowUp className="text-white" />
        </button>
      )}
    </div>
  );
};

export default UserInterface;