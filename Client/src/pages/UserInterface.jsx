import React, { useState, useEffect } from 'react';
import { Outlet } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import NavbarUser from '../components/NavbarUser';
import ChatInterface from "../components/ChatInterface";
import { FaArrowUp } from "react-icons/fa";
import { MessageCircle } from 'lucide-react';

const UserInterface = () => {
  const [showChat, setShowChat] = useState(false);
  const [showScrollButton, setShowScrollButton] = useState(false);
  const [isHoveringChat, setIsHoveringChat] = useState(false);
  const [isHoveringScroll, setIsHoveringScroll] = useState(false);

  // Control the display of the scroll button
  useEffect(() => {
    const handleScroll = () => {
      setShowScrollButton(window.scrollY > 200);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  // Animation variants for buttons
  const buttonVariants = {
    initial: { scale: 0, opacity: 0 },
    animate: { 
      scale: 1, 
      opacity: 1,
      transition: { type: "spring", stiffness: 260, damping: 20 }
    },
    exit: { 
      scale: 0, 
      opacity: 0,
      transition: { duration: 0.2 }
    },
    hover: {
      scale: 1.1,
      rotate: 360,
      transition: { duration: 0.3 }
    }
  };

  // Animation variants for button text
  const textVariants = {
    initial: { opacity: 0, x: -20 },
    animate: { opacity: 1, x: 0 },
    exit: { opacity: 0, x: -20 }
  };

  return (
    <div className="relative">
      <NavbarUser />
      <div>
        <Outlet />
      </div>

      {/* Chat Button */}
      <AnimatePresence>
        <motion.div
          className="fixed bottom-8 left-8 z-50 flex items-center"
          initial="initial"
          animate="animate"
          exit="exit"
          variants={buttonVariants}
        >
          <motion.button
            onHoverStart={() => setIsHoveringChat(true)}
            onHoverEnd={() => setIsHoveringChat(false)}
            onClick={() => setShowChat(true)}
            whileHover="hover"
            className="bg-[#8DD3BB] p-4 rounded-full hover:bg-gray-800 transition-all duration-300 shadow-lg flex items-center"
            aria-label="Open chat"
          >
            <MessageCircle className="text-white" size={24} />
          </motion.button>

          <AnimatePresence>
            {isHoveringChat && (
              <motion.span
                variants={textVariants}
                initial="initial"
                animate="animate"
                exit="exit"
                className="ml-2 bg-gray-800 text-white px-3 py-1 rounded-lg text-sm"
              >
                Open ChatBot
              </motion.span>
            )}
          </AnimatePresence>
        </motion.div>
      </AnimatePresence>

      {/* Chat Interface */}
      <AnimatePresence>
        {showChat && (
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 50 }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
          >
            <ChatInterface onClose={() => setShowChat(false)} />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Scroll to Top Button */}
      <AnimatePresence>
        {showScrollButton && (
          <motion.div
            className="fixed bottom-24 right-8 z-50 flex items-center"
            initial="initial"
            animate="animate"
            exit="exit"
            variants={buttonVariants}
          >
            <motion.button
              onHoverStart={() => setIsHoveringScroll(true)}
              onHoverEnd={() => setIsHoveringScroll(false)}
              onClick={scrollToTop}
              whileHover="hover"
              className="bg-gray-800 p-3 rounded-full hover:bg-[#8DD3BB] transition-all duration-300 shadow-lg flex items-center"
              aria-label="Scroll to top"
            >
              <FaArrowUp className="text-white" />
            </motion.button>
            <AnimatePresence>
              {isHoveringScroll && (
                <motion.span
                  variants={textVariants}
                  initial="initial"
                  animate="animate"
                  exit="exit"
                  className="mr-2 bg-gray-800 text-white px-3 py-1 rounded-lg text-sm"
                >
                  Back to Top
                </motion.span>
              )}
            </AnimatePresence>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default UserInterface;