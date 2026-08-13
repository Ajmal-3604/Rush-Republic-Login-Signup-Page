import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

/**
 * Blocks access unless the logged-in user's department is in
 * `allowedDepartments`. Admin is always granted access, matching the
 * backend's "Admin can access everything" rule.
 */
export default function RoleProtectedRoute({ allowedDepartments, children }) {
  const { user, loading } = useAuth();

  if (loading) return null;
  if (!user) return <Navigate to="/login" replace />;

  const isAllowed = user.department === 'ADMIN' || allowedDepartments.includes(user.department);
  if (!isAllowed) return <Navigate to="/unauthorized" replace />;

  return children;
}
