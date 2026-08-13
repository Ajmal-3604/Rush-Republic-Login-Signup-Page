import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Navbar.css';

const DEPARTMENT_LABELS = {
  ADMIN: 'Admin',
  SOCIAL_MEDIA: 'Social Media',
  PRODUCTION_COORDINATOR: 'Production Co-Ordinator',
  CLIENT_SERVICING: 'Client-Servicing',
};

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login', { replace: true });
  };

  return (
    <header className="rr-navbar">
      <div className="rr-navbar__brand">
        <span className="rr-navbar__mark">RR</span>
        <span className="rr-navbar__name">Rush Republic</span>
      </div>

      {user && (
        <div className="rr-navbar__right">
          <span className="rr-navbar__dept">{DEPARTMENT_LABELS[user.department]}</span>
          <button className="rr-navbar__logout" onClick={handleLogout}>
            Log out
          </button>
        </div>
      )}
    </header>
  );
}
