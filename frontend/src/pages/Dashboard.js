import { Link } from 'react-router-dom';

export default function DashboardPage() {
  return (
    <section className="card">
      <h1>Tableau de bord</h1>
      <p>Gérez vos salles, équipements et réservations depuis ce portail.</p>
      <div className="actions">
        <Link to="/rooms">Voir les salles</Link>
        <Link to="/reservations">Planifier une réunion</Link>
      </div>
    </section>
  );
}
