import React from 'react';
import './HeroSection.css';

const HeroSection = () => {
  return (
    <section className="hero-section">
      <div className="hero-container">
        <div className="hero-content">
          <h1 className="hero-title">
            Discover <span className="highlight">Morocco</span> Like Never Before!
          </h1>
          
          <p className="hero-description">
            Experience personalized journeys across Morocco tailored to your preferences and budget. Don’t miss the opportunity to join the global celebrations for the Africa Cup of Nations 2025 and the FIFA World Cup 2030.
          </p>

          <div className="hero-buttons">
            <a href="#" className="button button-primary">
              Start Your Adventure
            </a>
          </div>
        </div>

        <div className="hero-image">
          <img src="https://demo.themesberg.com/landwind/images/hero.png" alt="Traveler on a journey" />
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
