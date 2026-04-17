import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { useAuth } from '../context/AuthContext';

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: '', password: '' });
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    try {
      await login(form.username, form.password);
      navigate('/');
    } catch {
      setError('Identifiants invalides');
    }
  };

  return (
    <form className="card" onSubmit={handleSubmit}>
      <h1>Connexion</h1>
      <input placeholder="Nom d'utilisateur" value={form.username} onChange={(event) => setForm({ ...form, username: event.target.value })} />
      <input type="password" placeholder="Mot de passe" value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} />
      {error && <p className="error">{error}</p>}
      <button type="submit">Se connecter</button>
    </form>
  );
}
