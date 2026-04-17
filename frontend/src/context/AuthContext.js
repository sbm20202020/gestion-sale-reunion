import { createContext, useContext, useEffect, useMemo, useState } from 'react';

import api from '../services/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [tokens, setTokens] = useState(() => {
    const saved = localStorage.getItem('tokens');
    return saved ? JSON.parse(saved) : null;
  });
  const [user, setUser] = useState(null);

  useEffect(() => {
    if (tokens) {
      localStorage.setItem('tokens', JSON.stringify(tokens));
      api.defaults.headers.common.Authorization = `Bearer ${tokens.access}`;
      api.get('/auth/profile/').then((response) => setUser(response.data)).catch(() => logout());
    } else {
      localStorage.removeItem('tokens');
      delete api.defaults.headers.common.Authorization;
      setUser(null);
    }
  }, [tokens]);

  async function login(username, password) {
    const { data } = await api.post('/auth/token/', { username, password });
    setTokens(data);
  }

  async function register(payload) {
    await api.post('/auth/register/', payload);
  }

  function logout() {
    setTokens(null);
  }

  const value = useMemo(() => ({ user, login, register, logout }), [user]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
