import React from 'react';
import Navbar from '../components/Navbar';
import HeroSection from '../components/HeroSection';
import ServicesComponent from '../components/ServicesComponent';
import CarouselComponent from "../components/CarouselComponent";



const Home = () => {
  return (
    <div>
      <Navbar />
      <HeroSection />
      <ServicesComponent />
      <CarouselComponent />
    </div>
  );
};

export default Home;
