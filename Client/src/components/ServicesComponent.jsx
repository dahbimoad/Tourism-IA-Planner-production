import React from 'react';
import './ServicesComponent.css';
import MapIcon from '../assets/iteneraire.svg';
import LocationIcon from '../assets/map.svg';
import CostIcon from '../assets/cost.svg';
import TouristIcon from '../assets/Terroustique.svg';

const services = [
  {
    id: 1,
    icon: MapIcon,
    title: 'Personalized Itineraries',
    description: 'Optimize your travel experience with recommendations tailored to your preferences.'
  },
  {
    id: 2,
    icon: LocationIcon,
    title: 'Interactive Map',
    description: 'Visualize your routes and explore tourist destinations effortlessly.'
  },
  {
    id: 3,
    icon: CostIcon,
    title: 'Cost Predictions',
    description: 'Plan within your budget with accurate cost estimates.'
  },
  {
    id: 4,
    icon: TouristIcon,
    title: 'Tourist Information',
    description: 'Access detailed descriptions, stunning images, and reviews of must-visit locations'
  }
];

const ServicesComponent = () => {
  return (
    <section className="services-section">
      <h3 className="services-header">Services</h3>
      <h2 className="services-title">A Platform Designed To Simplify Your Travel</h2>
      <div className="services-container">
        {services.map((service) => (
          <div key={service.id} className="service-card">
            <div className="service-icon">
              <img src={service.icon} alt={service.title} />
            </div>
            <h3 className="service-title">{service.title}</h3>
            <p className="service-description">{service.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default ServicesComponent;
