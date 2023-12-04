import React, { useState, useEffect } from 'react';
import './flashMessage.css';

const FlashMessage = ({ message }) => {
  return <div className="flash-message">{message}</div>;
};

export default FlashMessage;