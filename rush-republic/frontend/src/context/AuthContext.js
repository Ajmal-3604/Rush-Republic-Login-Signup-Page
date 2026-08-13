import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import api from '../api/axios';

const AuthContext = createContext(null);

const DEPARTMENT_HOME_ROUTES = {
  ADMIN: '/admin-home',
  SOCIAL_MEDIA: '/social-media-home',
  PRODUCTION_COORDINATOR: '/production-coordinator-home',
  CLIENT_SERVICING: '/client-servicing-home',
};

export function getHomeRouteForDepartment(department) {
  return DEPARTMENT_HOME_ROUTES[department] || '/login';
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem('rr_user');
    return stored ? JSON.parse(stored) : null;
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Rehydrate the profile on refresh if a token exists.
    const token = localStorage.getItem('rr_access_token');
    if (!token) {
      setLoading(false);
      return;
    }
    api
      .get('/profile/')
      .then(({ data }) => {
        setUser(data);
        localStorage.setItem('rr_user', JSON.stringify(data));
      })
      .catch(() => {
        setUser(null);
      })
      .finally(() => setLoading(false));
  }, []);

  const login = useCallback(async (email, password) => {
    const { data } = await api.post('/login/', { email, password });
    localStorage.setItem('rr_access_token', data.access);
    localStorage.setItem('rr_refresh_token', data.refresh);
    localStorage.setItem('rr_user', JSON.stringify(data.user));
    setUser(data.user);
    return data.user;
  }, []);

  const signup = useCallback(async (payload) => {
    const { data } = await api.post('/signup/', payload);
    return data;
  }, []);

  const logout = useCallback(async () => {
    const refresh = localStorage.getItem('rr_refresh_token');
    try {
      if (refresh) {
        await api.post('/logout/', { refresh });
      }
    } catch {
      // Non-fatal: continue clearing local session even if the API call fails.
    } finally {
      localStorage.removeItem('rr_access_token');
      localStorage.removeItem('rr_refresh_token');
      localStorage.removeItem('rr_user');
      setUser(null);
    }
  }, []);

  const value = { user, loading, login, signup, logout };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within an AuthProvider');
  return ctx;
}
