import React, { useState, useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from '../contexts/AuthContext';
import { useProfile } from '../contexts/ProfileContext';

// Default avatar as base64 SVG
const defaultAvatar = `data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iI2ZmZmZmZiIgd2lkdGg9IjI0cHgiIGhlaWdodD0iMjRweCI+PHBhdGggZD0iTTEyIDEyYzIuMjEgMCA0LTEuNzkgNC00cy0xLjc5LTQtNC00LTQgMS43OS00IDQgMS43OSA0IDQgNHptMCAyYy0yLjY3IDAtOCAxLjMzLTggNHYyaDE2di0yYzAtMi42Ny01LjMzLTQtOC00eiIvPjxwYXRoIGQ9Ik0wIDBoMjR2MjRIMHoiIGZpbGw9Im5vbmUiLz48L3N2Zz4=`;

const Avatar = ({ imageUrl, name }) => (
  <div className="w-10 rounded-full overflow-hidden">
    {imageUrl ? (
      <img
        alt={`${name}'s avatar`}
        src={imageUrl}
        className="w-full h-full object-cover"
      />
    ) : (
      <img
        alt="Default avatar"
        src={defaultAvatar}
        className="w-full h-full object-cover bg-gray-600"
      />
    )}
  </div>
);

const NavLinks = ({ isMobile = false }) => {
  const links = [
    { href: "/home", text: "Home" },
    { href: "/dashboard/form", text: "Find Plan" },
    { href: "/dashboard/plans", text: "Plans" },
    { href: "/dashboard/FavouritesPlans", text: "Favourites" },
  ];

  const className = isMobile
    ? "menu menu-sm dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow"
    : "menu menu-horizontal px-1";

  return (
    <ul className={className}>
      {links.map(({ href, text }) => (
        <li key={href}>
          <a 
            href={href} 
            className={!isMobile ? "line-under hover:bg-transparent" : ""}
          >
            {text}
          </a>
        </li>
      ))}
    </ul>
  );
};

const NavbarUser = () => {
  const [menuActive, setMenuActive] = useState(false);
  const navigate = useNavigate();
  const { logout } = useContext(AuthContext);
  const { profile, getProfileImage } = useProfile();
  const [imagePreview, setImagePreview] = useState(null);

  useEffect(() => {
    const loadImage = async () => {
      if (profile) {
        const imageUrl = await getProfileImage();
        setImagePreview(imageUrl);
      }
    };
    loadImage();
  }, [profile, getProfileImage]);

  const handleLogout = async () => {
    const success = await logout();
    if (success) {
      navigate('/');
    }
  };

  return (
    <div className="navbar bg-base-200 shadow-md fixed z-40">
      <div className="navbar-start">
        <div className="dropdown lg:hidden">
          <div
            tabIndex={0}
            role="button"
            onClick={() => setMenuActive(!menuActive)}
            className="btn btn-ghost"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M4 6h16M4 12h8m-8 6h16"
              />
            </svg>
          </div>
          <NavLinks isMobile />
        </div>

        <div className="navbar-center hidden lg:flex">
          <NavLinks />
        </div>
      </div>

      <a className="btn btn-ghost text-xl">
        <span>TOURIST<span className="text-[#8DD3BB]">AI</span></span>
      </a>
      
      <div className="navbar-end">
        {/* Notifications */}
        

        {/* User Menu */}
        <div className="dropdown dropdown-end">
          <div
            tabIndex={0}
            role="button"
            className="btn btn-ghost btn-circle avatar"
          >
            <Avatar imageUrl={imagePreview} name={profile?.name} />
          </div>
          <ul
            tabIndex={0}
            className="menu menu-sm dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow"
          >
            <li>
              <a href="/dashboard/profil" className="justify-between">
                Profile
                <span className="badge">New</span>
              </a>
            </li>
            {/*<li><a>Settings</a></li>*/}
            <li>
              <a onClick={handleLogout} className="cursor-pointer">
                Logout
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default NavbarUser;