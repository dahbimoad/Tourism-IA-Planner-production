import React, { useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../contexts/AuthContext';

const GoogleAuthButton = () => {
  const { error, handleGoogleResponse } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    const loadGoogleScript = () => {
      return new Promise((resolve, reject) => {
        if (window.google) {
          resolve();
          return;
        }
        const script = document.createElement('script');
        script.src = 'https://accounts.google.com/gsi/client';
        script.async = true;
        script.defer = true;
        script.onload = resolve;
        script.onerror = reject;
        document.body.appendChild(script);
      });
    };

    const initializeGoogleButton = () => {
      if (!window.google) return;
      
      window.google.accounts.id.initialize({
        client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
        callback: async (response) => {
          const success = await handleGoogleResponse(response);
          if (success) {
            navigate('/dashboard/form');
          }
        },
        error_callback: (error) => {
          console.error('Google Sign-In Error:', error);
        }
      });

      window.google.accounts.id.renderButton(
        document.getElementById("googleButton"),
        {
          theme: "outline",
          size: "large",
          text: "sign_in_with",
          width: 250
        }
      );
    };

    const setup = async () => {
      try {
        await loadGoogleScript();
        initializeGoogleButton();
      } catch (error) {
        console.error('Google button setup failed:', error);
      }
    };

    setup();

    return () => {
      const script = document.querySelector('script[src="https://accounts.google.com/gsi/client"]');
      if (script) {
        document.body.removeChild(script);
      }
    };
  }, [handleGoogleResponse, navigate]);

  return (
    <div>
      <div id="googleButton"></div>
      {error && <p className="text-red-500 mt-2 text-sm">{error}</p>}
    </div>
  );
};

export default GoogleAuthButton;