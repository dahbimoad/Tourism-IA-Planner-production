import React, { useState } from "react";
import { FaTimes, FaPaperPlane, FaUser, FaRobot } from "react-icons/fa";

const ChatInterface = ({ onClose }) => {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([
    {
      text: "Hello! How can I help you with your Moroccan travel plans?",
      isBot: true,
    },
  ]);

  const handleSendMessage = () => {
    if (message.trim()) {
      // Add user message
      setMessages(prev => [...prev, { text: message, isBot: false }]);
      
      // Simulate bot response
      setTimeout(() => {
        setMessages(prev => [
          ...prev,
          { text: "Thank you for your message. Our team will respond shortly!", isBot: true },
        ]);
      }, 1000);

      setMessage("");
    }
  };

  return (
    <div className="fixed bottom-24 left-8 w-80 bg-white rounded-lg shadow-xl z-50">
      {/* Chat Header */}
      <div className="bg-gray-800 text-white p-4 rounded-t-lg flex justify-between items-center">
        <h3 className="font-semibold">Travel Assistant</h3>
        <button 
          onClick={onClose}
          className="hover:text-[#8DD3BB] transition-colors"
          aria-label="Close chat"
        >
          <FaTimes />
        </button>
      </div>

      {/* Chat Messages */}
      <div className="h-96 p-4 overflow-y-auto space-y-4">
        {messages.map((msg, index) => (
          <div 
            key={index}
            className={`flex ${msg.isBot ? "justify-start" : "justify-end"} gap-2`}
          >
            <div className={`p-3 rounded-lg max-w-[80%] ${
              msg.isBot 
                ? "bg-gray-100 text-gray-800"
                : "bg-[#8DD3BB] text-white"
            }`}>
              <div className="flex items-center gap-2 mb-1">
                {msg.isBot ? (
                  <FaRobot className="text-gray-600" />
                ) : (
                  <FaUser className="text-white" />
                )}
                <span className="text-xs font-medium">
                  {msg.isBot ? "Travel Bot" : "You"}
                </span>
              </div>
              <p className="text-sm">{msg.text}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Message Input */}
      <div className="p-4 border-t border-gray-200">
        <div className="flex gap-2">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
            placeholder="Type your message..."
            className="w-full px-3 py-2 border rounded-lg text-black focus:outline-none focus:ring-2 focus:ring-[#2ba67b]"
          />
          <button
            onClick={handleSendMessage}
            className="bg-[#8DD3BB] text-white p-2 rounded-lg hover:bg-[#7abfa8] transition-colors"
            aria-label="Send message"
          >
            <FaPaperPlane />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;