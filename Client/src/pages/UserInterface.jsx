import React from 'react';
import { Outlet } from 'react-router-dom';
import NavbarUser from '../components/NavbarUser';

const UserInterface = () => {
  return (
    <div>
      <NavbarUser />
      <div>
        {/* Render the nested routes */}
        <Outlet />
      </div>
    </div>
  );
};

export default UserInterface;
