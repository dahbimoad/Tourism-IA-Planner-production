import React, { useState } from 'react';
import './Navbar.css';
import { useNavigate } from "react-router-dom";

const NavBar = () => {
  const [menuActive, setMenuActive] = useState(false);
  const navigate = useNavigate();

  const toggleMenu = () => {
    setMenuActive(!menuActive);
  };

  return (
    <div className="navbar bg-base-200 shadow-md fixed z-40">
      <div className="navbar-start">
        <div className="dropdown">
          <div tabIndex={0} role="button" onClick={toggleMenu} className="btn btn-ghost lg:hidden">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M4 6h16M4 12h8m-8 6h16" />
            </svg>
          </div>
          <ul
            tabIndex={0}
            className="menu menu-sm dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow">
            <li><a href="#home">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#destinations">Destinations</a></li>
            <li><a href="#contact">Contact</a></li>
            <li><a href="#reviews">Reviews</a></li>
          </ul>
        </div>
        <a className="btn btn-ghost text-xl">
          <span>
            L<span className="text-[#8DD3BB]">O</span>GO
          </span>
        </a>
      </div>
      <div className="navbar-center hidden lg:flex">
        <ul className="menu menu-horizontal px-1">
          <li><a href="#home" className="line-under hover:bg-transparent">Home</a></li>
          <li><a href="#about" className="line-under hover:bg-transparent">About</a></li>
          <li><a href="#destinations" className="line-under hover:bg-transparent">Destinations</a></li>
          <li><a href="#contact" className="line-under hover:bg-transparent">Contact</a></li>
          <li><a href="#reviews" className="line-under hover:bg-transparent">Reviews</a></li>
        </ul>
      </div>
      <div className="navbar-end">
        <a className="btn bg-[#8DD3BB] text-black hover:bg-black hover:text-[#8DD3BB] rounded-full" onClick={() => navigate("/login")}>Login</a>
      </div>
    </div>
  );
};

export default NavBar;
