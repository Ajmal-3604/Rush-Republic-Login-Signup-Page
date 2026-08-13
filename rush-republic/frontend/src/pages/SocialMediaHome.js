import React, { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import api from '../api/axios';
import './Home.css';
import logo from '../assets/rush-republic-logo.png';

export default function SocialMediaHome() {
  const [user, setUser] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    api
      .get('/social-media/')
      .then(({ data }) => setUser(data.user))
      .catch(() => setError('Could not load your details.'));
  }, []);

  return (
    <div className="rr-page">
      <Navbar />
      <div className="rr-page__body">
        <div className="rr-page__eyebrow">Social Media</div>
        <h1 className="rr-page__title">This is Social Media Home Page</h1>

        {error && <p>{error}</p>}

        {user && (
          <div className="rr-card">
            <div className="rr-card__label">User details</div>
            <div className="rr-card__row">
              <span className="rr-card__row-label">Username</span>
              <span className="rr-card__row-value">{user.username}</span>
            </div>
            <div className="rr-card__row">
              <span className="rr-card__row-label">Email</span>
              <span className="rr-card__row-value">{user.email}</span>
            </div>
            <div className="rr-card__row">
              <span className="rr-card__row-label">Contact</span>
              <span className="rr-card__row-value">{user.contact}</span>
            </div>
            <div className="rr-card__row">
              <span className="rr-card__row-label">Department</span>
              <span className="rr-card__row-value">{user.department_display}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
