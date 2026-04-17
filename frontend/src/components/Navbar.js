import { Link, useNavigate } from 'react-router-dom';

import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const onLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="navbar">
      <Link to="/" className="brand">
        Gestion Salles
      </Link>
      <nav>
        {user ? (
          <>
            <Link to="/rooms">Salles</Link>
            <Link to="/reservations">Réservations</Link>
            <Link to="/profile">Profil</Link>
            <button onClick={onLogout}>Déconnexion</button>
          </>
        ) : (
          <>
            <Link to="/login">Connexion</Link>
            <Link to="/register">Inscription</Link>
          </>
        )}
      </nav>
    </header>
  );
}
