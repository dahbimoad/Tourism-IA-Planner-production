// Navbar.jsx
import React, { useState } from 'react';
import './NavBar.css';

const NavBar = () => {
  const [menuActive, setMenuActive] = useState(false);

  const toggleMenu = () => {
    setMenuActive(!menuActive);
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <a href="#" className="logo">
          LOGO<span className="logo-icon">▲</span>
        </a>
        
        <button 
          className="menu-toggle" 
          aria-label="Toggle menu" 
          onClick={toggleMenu}
        >
          <span className="bar"></span>
          <span className="bar"></span>
          <span className="bar"></span>
        </button>

        <div className={`nav-menu ${menuActive ? 'active' : ''}`}>
          <ul className="nav-list">
            <li className="nav-item"><a href="#" className="nav-link">Home</a></li>
            <li className="nav-item"><a href="#" className="nav-link">About</a></li>
            <li className="nav-item"><a href="#" className="nav-link">Login</a></li>
            <li className="nav-item"><a href="#" className="nav-link sign-up">Sign Up</a></li>
            <li className="nav-item language-selector">
              <a href="#" className="nav-link">EN <span className="chevron">▼</span></a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default NavBar;
