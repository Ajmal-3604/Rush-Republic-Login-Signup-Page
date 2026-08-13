import React, { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import api from '../api/axios';
import './Home.css';

export default function AdminHome() {
  const [data, setData] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    api
      .get('/admin-dashboard/')
      .then(({ data }) => setData(data))
      .catch(() => setError('Could not load dashboard data.'));
  }, []);

  return (
    <div className="rr-page">
      <Navbar />
      <div className="rr-page__body">
        <div className="rr-page__eyebrow">Admin</div>
        <h1 className="rr-page__title">This is Admin Home Page</h1>

        {error && <p>{error}</p>}

        {data && (
          <div className="rr-stats-grid">
            <div className="rr-stat">
              <div className="rr-stat__label">Total users</div>
              <div className="rr-stat__value">{data.total_users}</div>
            </div>

            <div className="rr-stat">
              <div className="rr-stat__label">Departments</div>
              <div className="rr-stat__value">{Object.keys(data.users_by_department).length}</div>
            </div>

            <div className="rr-stat rr-stat--wide">
              <div className="rr-stat__label">Users by department</div>
              <div className="rr-dept-breakdown">
                {Object.entries(data.users_by_department).map(([dept, count]) => (
                  <div className="rr-dept-breakdown__row" key={dept}>
                    <span>{dept}</span>
                    <span>{count}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
