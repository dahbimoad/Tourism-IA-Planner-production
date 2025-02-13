import React, { useState, useEffect, useRef } from "react";
import { ChatProvider, useChat } from '../contexts/ChatContext';
import { 
  MessageCircle, 
  X, 
  Send, 
  User, 
  Bot, 
  ChevronDown,
  Loader
} from "lucide-react";

const ChatInterface = ({ onClose }) => {
  const [message, setMessage] = useState("");
  const [isExpanded, setIsExpanded] = useState(true);
  const { messages, sendMessage, loading, error } = useChat();
  const messagesEndRef = useRef(null);
  const [isVisible, setIsVisible] = useState(true);

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
    const isBot = msg.type === 'bot';
    const bubbleClass = isBot 
      ? "bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100" 
      : "bg-[#8DD3BB] dark:bg-[#8DD3BB]/90 text-gray-900";

    if (msg.status === "error") {
      return (
        <div className="flex justify-center mb-4 animate-fadeIn">
          <div className="bg-red-100 dark:bg-red-900/50 text-red-700 dark:text-red-200 p-4 rounded-xl max-w-[85%] text-center shadow-sm">
            {msg.response}
          </div>
        </div>
      );
    }

    return (
      <div className={`flex items-end gap-2 mb-4 ${isBot ? "justify-start" : "justify-end"} animate-slideIn`}>
        {isBot && (
          <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
            <Bot size={18} className="text-gray-600 dark:text-gray-300" />
          </div>
        )}
        <div className={`${bubbleClass} p-4 rounded-2xl shadow-sm max-w-[75%] transition-all`}>
          <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content || msg.response}</p>
        </div>
        {!isBot && (
          <div className="flex-shrink-0 w-8 h-8 rounded-full bg-[#8DD3BB]/20 dark:bg-[#8DD3BB]/20 flex items-center justify-center">
            <User size={18} className="text-[#8DD3BB] dark:text-[#8DD3BB]" />
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="fixed inset-0 z-50 pointer-events-none">
      <div 
        className={`
          absolute left-4 bottom-4 
          w-[380px] max-w-[95vw]
          bg-white dark:bg-gray-900 
          rounded-2xl shadow-2xl
          transform transition-all duration-300 ease-out
          ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}
          ${isExpanded ? 'h-[600px]' : 'h-16'}
          overflow-hidden
          border border-gray-200 dark:border-gray-800
          pointer-events-auto
          backdrop-blur-lg
        `}
      >
        {/* Header */}
        <div 
          onClick={() => setIsExpanded(!isExpanded)}
          className="bg-white dark:bg-gray-900 px-4 py-3 
            border-b border-gray-200 dark:border-gray-800
            flex items-center justify-between
            cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800/50
            transition-colors duration-200
            relative z-10"
        >
          <div className="flex items-center gap-2">
            <MessageCircle className="text-[#8DD3BB] dark:text-[#8DD3BB]" size={20} />
            <h3 className="font-medium text-gray-900 dark:text-gray-100">Chat Assistant</h3>
          </div>
          <div className="flex items-center gap-2">
            <ChevronDown 
              size={20}
              className={`text-gray-600 dark:text-gray-400 transition-transform duration-200 
                ${isExpanded ? 'rotate-180' : 'rotate-0'}`}
            />
            <button
              onClick={(e) => {
                e.stopPropagation();
                setIsVisible(false);
                setTimeout(onClose, 300);
              }}
              className="p-1 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full transition-colors"
              aria-label="Close chat"
            >
              <X size={18} className="text-gray-600 dark:text-gray-400" />
            </button>
          </div>
        </div>

        {/* Messages */}
        {isExpanded && (
          <div className="h-[calc(100%-120px)] p-4 overflow-y-auto space-y-2 bg-white dark:bg-gray-900 relative z-10">
            {messages.map((msg, index) => (
              <MessageBubble key={msg.id || index} msg={msg} index={index} />
            ))}

            {loading && (
              <div className="flex items-center gap-2 p-3 bg-gray-100 dark:bg-gray-800 rounded-xl animate-pulse">
                <Loader className="animate-spin text-gray-600 dark:text-gray-400" size={18} />
                <span className="text-sm text-gray-600 dark:text-gray-400">Typing...</span>
              </div>
            )}

            {error && (
              <div className="flex justify-center mb-4">
                <div className="bg-red-100 dark:bg-red-900/50 text-red-700 dark:text-red-200 p-4 rounded-xl max-w-[85%] text-center">
                  {error}
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        )}

        {/* Input */}
        {isExpanded && (
          <div className="absolute bottom-0 left-0 right-0 p-4 bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800 relative z-10">
            <div className="flex gap-2">
              <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
                placeholder="Type a message..."
                disabled={loading}
                className="w-full px-4 py-2 rounded-xl text-gray-900 dark:text-white 
                  bg-gray-100 dark:bg-gray-800 
                  border-0 focus:ring-2 focus:ring-[#8DD3BB] dark:focus:ring-[#8DD3BB]/70
                  placeholder-gray-500 dark:placeholder-gray-400
                  disabled:opacity-50 disabled:cursor-not-allowed
                  transition-all duration-200"
              />
              <button
                onClick={handleSendMessage}
                disabled={loading || !message.trim()}
                className="p-2 rounded-xl bg-[#8DD3BB] dark:bg-[#8DD3BB]/90 text-gray-900
                  hover:bg-[#7EC3AB] dark:hover:bg-[#8DD3BB]
                  disabled:opacity-50 disabled:cursor-not-allowed
                  transition-all duration-200
                  flex items-center justify-center min-w-[44px]"
              >
                {loading ? (
                  <Loader className="animate-spin" size={18} />
                ) : (
                  <Send size={18} />
                )}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

const ChatInterfaceWithProvider = ({ onClose }) => (
  <ChatProvider>
    <ChatInterface onClose={onClose} />
  </ChatProvider>
);

export default ChatInterfaceWithProvider;