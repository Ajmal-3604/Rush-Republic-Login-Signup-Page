import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';

import ProtectedRoute from './components/ProtectedRoute';
import RoleProtectedRoute from './components/RoleProtectedRoute';

import Login from './pages/Login';
import Signup from './pages/Signup';
import AdminHome from './pages/AdminHome';
import SocialMediaHome from './pages/SocialMediaHome';
import ProductionCoordinatorHome from './pages/ProductionCoordinatorHome';
import ClientServicingHome from './pages/ClientServicingHome';
import Unauthorized from './pages/Unauthorized';

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/unauthorized" element={<Unauthorized />} />

          <Route
            path="/admin-home"
            element={
              <RoleProtectedRoute allowedDepartments={['ADMIN']}>
                <AdminHome />
              </RoleProtectedRoute>
            }
          />

          <Route
            path="/social-media-home"
            element={
              <RoleProtectedRoute allowedDepartments={['SOCIAL_MEDIA']}>
                <SocialMediaHome />
              </RoleProtectedRoute>
            }
          />

          <Route
            path="/production-coordinator-home"
            element={
              <RoleProtectedRoute allowedDepartments={['PRODUCTION_COORDINATOR']}>
                <ProductionCoordinatorHome />
              </RoleProtectedRoute>
            }
          />

          <Route
            path="/client-servicing-home"
            element={
              <RoleProtectedRoute allowedDepartments={['CLIENT_SERVICING']}>
                <ClientServicingHome />
              </RoleProtectedRoute>
            }
          />

          {/* Fallback: any authenticated user hitting an unknown route goes to login */}
          <Route
            path="*"
            element={
              <ProtectedRoute>
                <Navigate to="/login" replace />
              </ProtectedRoute>
            }
          />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
