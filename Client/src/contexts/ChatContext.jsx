import { createContext, useContext, useState, useCallback } from 'react';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  

  // New state to store the latest API response
  const [latestResponse, setLatestResponse] = useState(null);

  const sendMessage = useCallback(async (message) => {
    try {
      setLoading(true);
      setError(null);

      const response = await axios.post(`${API_URL}/api/chat`, {
        message: message
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      // Validate the response structure
      if (response.data && response.data.status === 'success') {
        // Store the complete API response
        setLatestResponse(response.data);

        // Update messages state with both user and bot messages
        const userMessage = { type: 'user', content: message };
        const botMessage = { 
          type: 'bot', 
          content: response.data.response 
        };

        setMessages(prevMessages => [
          ...prevMessages, 
          userMessage, 
          botMessage
        ]);

        setSuccessMessage('Message sent successfully');
        
        // Clear success message after 3 seconds
        setTimeout(() => setSuccessMessage(null), 3000);

        return response.data;
      } else {
        throw new Error('Message sending failed');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to send message');
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  // Clear messages functionality
  const clearMessages = useCallback(() => {
    setMessages([]);
    setLatestResponse(null);
  }, []);

  return (
    <ChatContext.Provider
      value={{
        messages,
        loading,
        error,
        successMessage,
        latestResponse,  // Expose the latest API response
        sendMessage,
        clearMessages,
        // Optional: method to directly access the latest bot response
        getLatestBotResponse: () => latestResponse?.response
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};

// Custom hook to use the ChatContext
export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};