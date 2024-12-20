import React, { useState } from 'react' // Importation de React et de l’hook useState pour la gestion de l’état local du composant
import Carousel from 'react-multi-carousel' // Importation du composant de carousel à partir de la bibliothèque react-multi-carousel
import 'react-multi-carousel/lib/styles.css' // Importation des styles CSS pour le carousel
import { IoIosArrowForward } from 'react-icons/io' // Importation de l'icône flèche à partir de la bibliothèque react-icons

// Importation des images des destinations touristiques
import Agadir from '../assets/Agadir.jpg'
import Casablanca from '../assets/Casablanca.jpg'
import Chefchaouen from '../assets/Chefchaouen.jpg'
import Dakhla from '../assets/Dakhla.jpg'
import Marrakech from '../assets/Marrakech.jpg'

// Configuration du carousel pour définir le nombre d’éléments à afficher selon la taille de l’écran
const responsive = {
  superLargeDesktop: { // Configuration pour les très grands écrans
    breakpoint: { max: 4000, min: 3000 },
    items: 4, // Affiche 4 éléments
  },
  desktop: { // Configuration pour les écrans de bureau
    breakpoint: { max: 3000, min: 1024 },
    items: 4, // Affiche 4 éléments
  },
  tablet: { // Configuration pour les tablettes
    breakpoint: { max: 1024, min: 464 },
    items: 3, // Affiche 3 éléments
  },
  module: { // Configuration pour les petits écrans mobiles
    breakpoint: { max: 464, min: 0 },
    items: 1, // Affiche 1 élément
  },
}

// Composant ExploreItem qui représente chaque carte d'une destination à afficher dans le carousel
const ExploreItem = ({ image, country }) => {
  return (
    <div className="relative group overflow-hidden rounded-[10px] shadow-lg"> 
      {/* Conteneur principal de l'item avec des styles pour l’effet de survol */}
      <img
        src={image} // Chemin de l’image de la destination
        alt={country} // Texte alternatif pour l’accessibilité
        className="w-full h-[350px] object-cover rounded-[10px] transition-transform duration-700 ease-in-out group-hover:scale-125 " // Style pour l'image
      />

      <div className="absolute bottom-0 w-full bg-black bg-opacity-50 py-5 flex flex-col items-center justify-center transition-all duration-300 group-hover:bg-white group-hover:bg-opacity-100">
        {/* Conteneur contenant le nom du pays et le bouton de navigation */}
        <p className="text-green text-xl font-bold flex flex-col">
          <span className="text-white text-2xl group-hover:text-gray-800">
            {country} {/* Affichage dynamique du nom de la destination */}
          </span>
        </p>
      </div>
    </div>
  )
}

// Composant principal du carousel
const CarouselComponent = () => {
  const [currentSlide, setCurrentSlide] = useState(0) // État local pour suivre la diapositive actuelle

  const handleAfterChange = (_, state) => {
    setCurrentSlide(state.currentSlide) // Met à jour l’état lorsque la diapositive change
  }

  // Données des destinations (image et nom du pays) à afficher dans le carousel
  const destinations = [
    { country: 'Agadir', image: Agadir },
    { country: 'Casablanca', image: Casablanca },
    { country: 'Chefchaouen', image: Chefchaouen },
    { country: 'Dakhla', image: Dakhla },
    { country: 'Marrakech', image: Marrakech },
  ]

  return (
    <div className="max-w-[1320px] mx-auto"> {/* Conteneur principal pour centrer le contenu */}
      <div className="py-16"> {/* Marges verticales */}
        <div className="flex flex-col items-center"> 
          <div className="relative w-fit px-8 py-2 flex items-center justify-center">
            <span className="bg-green rounded-md opacity-15 absolute w-full h-full z-10"></span> {/* Fond coloré d’arrière-plan */}
            <h6 className="text-green relative font-semibold">
              Popular Cites {/* Titre de la section */}
            </h6>
          </div>
          <h3 className="lg:text-5xl text-3xl font-bold pb-8 text-center py-4">
            Discover True Adventures in <span className='text-[#8DD3BB]'>Morocco</span> {/* Sous-titre */}
          </h3>
        </div>
        
        <Carousel
          responsive={responsive} // Configuration du carousel
          infinite // Le carousel tourne en boucle
          autoPlay={true} // Lecture automatique des diapositives
          itemClass="px-2 pb-6" // Espacement entre les items
          afterChange={handleAfterChange} // Met à jour la diapositive actuelle lors du changement
        >
          {destinations.map((item, index) => (
            <ExploreItem key={index} country={item.country} image={item.image} /> // Affiche chaque destination dans le carousel
          ))}
        </Carousel>
      </div>
    </div>
  )
}

export default CarouselComponent // Exportation du composant principal pour l'utiliser dans d'autres parties de l'application
