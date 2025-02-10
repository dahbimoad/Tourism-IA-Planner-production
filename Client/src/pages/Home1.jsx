import React from 'react';
import NavBar1 from '../components/NavBar1';
import AboutSection from '../components/AboutSection';
import HeroSection from '../components/HeroSection';
import ContactSection from '../components/ContactSection';
import ReviewsSection from '../components/ReviewsSection';
import CarouselComponent from "../components/CarouselComponent";
import FooterSection from "../components/FooterSection";



const Home1 = () => {
  return (
    <div>
      <NavBar1 />
      <HeroSection/>
      <AboutSection />
      <CarouselComponent />
      <ContactSection />
      <ReviewsSection />
      <FooterSection />
    </div>
  );
};

export default Home1;
