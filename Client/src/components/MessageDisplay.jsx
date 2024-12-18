import React from 'react';
import './MessageDisplay.css';

const MessageDisplay = ({ message }) => {
  return (
    <div className="message-container">
      <p>Message de l'API : <strong>{message}</strong></p>
    </div>
  );
};

export default MessageDisplay;
