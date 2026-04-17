import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { useAuth } from '../context/AuthContext';

export default function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    phone: '',
    department: '',
  });

  const handleSubmit = async (event) => {
    event.preventDefault();
    await register(form);
    navigate('/login');
  };

  return (
    <form className="card" onSubmit={handleSubmit}>
      <h1>Inscription</h1>
      {Object.entries(form).map(([key, value]) => (
        <input
          key={key}
          type={key === 'password' ? 'password' : 'text'}
          placeholder={key}
          value={value}
          onChange={(event) => setForm({ ...form, [key]: event.target.value })}
        />
      ))}
      <button type="submit">Créer un compte</button>
    </form>
  );
}
