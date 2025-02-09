// ChatContext.jsx
import { createContext, useContext, useState, useCallback } from 'react';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const sendMessage = useCallback(async (message) => {
    try {
      setLoading(true);
      setError(null);

      // Add user message immediately
      const userMessage = { type: 'user', content: message };
      setMessages(prev => [...prev, userMessage]);

      const response = await axios.post(`${API_URL}/api/chat`, {
        message: message
      });

      const data = response.data;

      // Handle error responses from the API
      if (data.status === 'error') {
        // Add error message to chat
        const errorMessage = {
          type: 'bot',
          status: 'error',
          response: data.response || 'An error occurred. Please try again later.'
        };
        setMessages(prev => [...prev, errorMessage]);
        setError(data.response);
        return;
      }

      // Add successful bot response
      const botMessage = {
        type: 'bot',
        content: data.response,
        id: Date.now()
      };
      setMessages(prev => [...prev, botMessage]);

    } catch (error) {
      console.error('Chat error:', error);
      // Add error message to chat
      const errorMessage = {
        type: 'bot',
        status: 'error',
        response: '⚠️ The chat service is currently unavailable. Please try again later.'
      };
      setMessages(prev => [...prev, errorMessage]);
      setError('Service temporarily unavailable');
    } finally {
      setLoading(false);
    }
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  return (
    <ChatContext.Provider
      value={{
        messages,
        loading,
        error,
        sendMessage,
        clearMessages
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};