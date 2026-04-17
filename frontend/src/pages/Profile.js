import { useEffect, useState } from 'react';

import api from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function ProfilePage() {
  const { user } = useAuth();
  const [form, setForm] = useState({ first_name: '', last_name: '', email: '', phone: '', department: '' });

  useEffect(() => {
    if (user) {
      setForm({
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        email: user.email || '',
        phone: user.phone || '',
        department: user.department || '',
      });
    }
  }, [user]);

  const save = async (event) => {
    event.preventDefault();
    await api.patch('/auth/profile/', form);
  };

  return (
    <form className="card" onSubmit={save}>
      <h1>Profil</h1>
      {Object.entries(form).map(([key, value]) => (
        <input
          key={key}
          type="text"
          placeholder={key}
          value={value}
          onChange={(event) => setForm({ ...form, [key]: event.target.value })}
        />
      ))}
      <button type="submit">Enregistrer</button>
    </form>
  );
}
