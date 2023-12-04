import React, { useState, useEffect } from 'react';
import './chatWindow.css';

const ChatWindow = ({ messages, windowSize }) => {
  const [newMessage, setNewMessage] = useState(null);

  useEffect(() => {
    // Trigger animation when a new message is added
    if (messages.length > 0) {
      setNewMessage(messages[messages.length - 1]);
      setTimeout(() => {
        setNewMessage(null);
      }, 1000);
    }
  }, [messages]);

  return (
    <div className="chat-window" style={{ height: windowSize }}>
      <div className="message-list">
        {messages.map((message, index) => (
          <div key={index} className="message">
            {message}
          </div>
        ))}
        {newMessage && (
          <div className="new-message" onAnimationEnd={() => setNewMessage(null)}>
            {newMessage}
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatWindow;