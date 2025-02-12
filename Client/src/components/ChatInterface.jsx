import React, { useState, useEffect, useRef } from "react";
import { FaTimes, FaPaperPlane, FaUser, FaRobot, FaSpinner, FaChevronDown } from "react-icons/fa";
import { ChatProvider, useChat } from '../contexts/ChatContext';

const ChatInterface = ({ onClose }) => {
  const [message, setMessage] = useState("");
  const [isExpanded, setIsExpanded] = useState(true);
  const { messages, sendMessage, loading, error } = useChat();
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSendMessage = async () => {
    if (message.trim()) {
      await sendMessage(message);
      setMessage("");
    }
  };

  const MessageBubble = ({ msg, index }) => {
    // Handle error responses
    if (msg.status === "error") {
      return (
        <div className="flex justify-center mb-4">
          <div className="bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-200 p-3 rounded-lg max-w-[80%] text-center">
            {msg.response}
          </div>
        </div>
      );
    }

    return (
      <div
        key={index}
        className={`flex ${msg.type === 'bot' ? "justify-start" : "justify-end"} gap-2 mb-2`}
      >
        <div
          className={`p-3 rounded-lg max-w-[80%] ${
            msg.type === 'bot' 
              ? "bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 shadow-sm"
              : "bg-[#8DD3BB] dark:bg-[#1b7d63] text-black dark:text-white"
          }`}
          aria-label={`Message from ${msg.type === 'bot' ? 'Travel Bot' : 'You'}`}
        >
          <div className="flex items-center gap-2 mb-1">
            {msg.type === 'bot' ? (
              <FaRobot className="text-gray-600 dark:text-gray-400" aria-hidden="true" />
            ) : (
              <FaUser className="text-gray-800 dark:text-gray-200" aria-hidden="true" />
            )}
            <span className="text-xs font-medium">
              {msg.type === 'bot' ? "Travel Bot" : "You"}
            </span>
          </div>
          <p className="text-sm break-words whitespace-pre-wrap">{msg.content || msg.response}</p>
        </div>
      </div>
    );
  };

  return (
    <div className={`
      fixed left-2 sm:left-4 bottom-4 sm:bottom-20 
      w-[95%] sm:w-[80%] md:w-full md:max-w-md 
      bg-white dark:bg-gray-900 
      rounded-lg shadow-xl z-50 
      transition-all duration-300 ease-in-out
      ${isExpanded ? 'h-[500px] sm:h-[550px] md:h-[500px]' : 'h-16'}
      overflow-hidden
    `}>
      {/* Header */}
      <div
        className="bg-gray-800 dark:bg-gray-900 text-white p-4 rounded-t-lg flex justify-between items-center cursor-pointer"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <h3 className="font-semibold flex items-center text-sm sm:text-base">
          Travel Assistant
          <FaChevronDown
            className={`ml-2 transition-transform duration-300 
              ${isExpanded ? 'rotate-180' : 'rotate-0'}`}
          />
        </h3>
        <button
          onClick={(e) => {
            e.stopPropagation();
            onClose();
          }}
          className="hover:text-[#8DD3BB] transition-colors"
          aria-label="Close chat"
        >
          <FaTimes />
        </button>
      </div>

      {/* Messages Container */}
      {isExpanded && (
        <div className="h-[calc(100%-130px)] p-2 sm:p-4 overflow-y-auto space-y-2 custom-scrollbar dark:bg-gray-800">
          {messages.map((msg, index) => (
            <MessageBubble key={msg.id || index} msg={msg} index={index} />
          ))}

          {loading && (
            <div className="flex justify-start items-center gap-2 p-3 bg-gray-100 dark:bg-gray-700 rounded-lg">
              <FaSpinner className="animate-spin text-gray-600 dark:text-gray-400" />
              <span className="text-sm text-gray-600 dark:text-gray-400">Travel Bot is typing...</span>
            </div>
          )}

          {error && (
            <div className="flex justify-center mb-4">
              <div className="bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-200 p-3 rounded-lg max-w-[80%] text-center">
                {error}
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      )}

      {/* Message Input */}
      {isExpanded && (
        <div className="absolute bottom-0 left-0 right-0 p-2 sm:p-4 border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
          <div className="flex gap-2">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
              placeholder="Type your message..."
              disabled={loading}
              className="w-full px-3 py-2 border rounded-lg text-black dark:text-white 
                bg-white dark:bg-gray-800 border-gray-300 dark:border-gray-600
                focus:outline-none focus:ring-2 focus:ring-[#2ba67b] dark:focus:ring-[#1b7d63] 
                disabled:opacity-50 disabled:cursor-not-allowed"
              aria-label="Type your message"
            />
            <button
              onClick={handleSendMessage}
              disabled={loading || !message.trim()}
              className="bg-[#8DD3BB] dark:bg-[#1b7d63] text-black dark:text-white p-2 rounded-lg 
                hover:bg-[#2ba67b] dark:hover:bg-[#154e3e] 
                transition-colors disabled:opacity-50 disabled:cursor-not-allowed 
                flex items-center justify-center min-w-[40px]"
              aria-label="Send message"
            >
              {loading ? <FaSpinner className="animate-spin" /> : <FaPaperPlane />}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

const ChatInterfaceWithProvider = ({ onClose }) => {
  return (
    <ChatProvider>
      <ChatInterface onClose={onClose} />
    </ChatProvider>
  );
};

export default ChatInterfaceWithProvider;