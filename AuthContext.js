
// contexts/AuthContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing auth token
    const token = localStorage.getItem('auth_token');
    if (token) {
      setIsAuthenticated(true);
      setUser({ role: 'analyst', name: 'Demo User' });
    }
    setLoading(false);
  }, []);

  const login = async (credentials) => {
    try {
      // Mock login - replace with real authentication
      if (credentials.email === 'demo@example.com' && credentials.password === 'demo') {
        const token = 'demo-token';
        localStorage.setItem('auth_token', token);
        setIsAuthenticated(true);
        setUser({ role: 'analyst', name: 'Demo User', email: credentials.email });
        return { success: true };
      }
      return { success: false, error: 'Invalid credentials' };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    setIsAuthenticated(false);
    setUser(null);
  };

  const value = {
    isAuthenticated,
    user,
    loading,
    login,
    logout
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
