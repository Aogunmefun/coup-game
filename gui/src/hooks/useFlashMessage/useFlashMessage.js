import { useState, useEffect } from 'react';
import FlashMessage from '../../components/flashMessage/flashMessage';

const useFlashMessage = () => {
  const [message, setMessage] = useState(null);

  const showMessage = (text) => {
    setMessage(text);
    setTimeout(() => {
      setMessage(null);
    }, 1000);
  };

  return { showMessage, FlashMessageComponent: message && <FlashMessage message={message} className="show" /> };
};

export default useFlashMessage;