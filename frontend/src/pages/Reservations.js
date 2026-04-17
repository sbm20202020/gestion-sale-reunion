import { useCallback, useEffect, useState } from 'react';

import ReservationCalendar from '../components/ReservationCalendar';
import api from '../services/api';

export default function ReservationsPage() {
  const [reservations, setReservations] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState({
    room: '',
    title: '',
    description: '',
    start_datetime: '',
    end_datetime: '',
    participants: [],
    is_recurring: false,
    frequency: 'weekly',
    interval: 1,
    count: '',
  });
  const [filters, setFilters] = useState({ room: '', user: '', start: '', end: '' });

  const fetchReservations = useCallback(() => {
    const params = Object.fromEntries(Object.entries(filters).filter(([, value]) => value));
    api.get('/reservations/reservations/', { params }).then((response) => setReservations(response.data));
  }, [filters]);

  useEffect(() => {
    api.get('/rooms/rooms/').then((response) => setRooms(response.data));
    api.get('/auth/participants/').then((response) => setUsers(response.data));
  }, []);

  useEffect(() => {
    fetchReservations();
  }, [fetchReservations]);

  const createReservation = async (event) => {
    event.preventDefault();
    const payload = {
      room: Number(form.room),
      title: form.title,
      description: form.description,
      start_datetime: form.start_datetime,
      end_datetime: form.end_datetime,
      participants: form.participants.map(Number),
      is_recurring: form.is_recurring,
    };
    if (form.is_recurring) {
      payload.recurrence_rule = {
        frequency: form.frequency,
        interval: Number(form.interval),
        count: form.count ? Number(form.count) : null,
      };
    }
    await api.post('/reservations/reservations/', payload);
    fetchReservations();
  };

  return (
    <section className="card">
      <h1>Réservations</h1>
      <div className="filters">
        <select value={filters.room} onChange={(event) => setFilters({ ...filters, room: event.target.value })}>
          <option value="">Toutes les salles</option>
          {rooms.map((room) => (
            <option key={room.id} value={room.id}>
              {room.name}
            </option>
          ))}
        </select>
        <select value={filters.user} onChange={(event) => setFilters({ ...filters, user: event.target.value })}>
          <option value="">Tous les organisateurs</option>
          {users.map((user) => (
            <option key={user.id} value={user.id}>
              {user.username}
            </option>
          ))}
        </select>
        <input type="date" value={filters.start} onChange={(event) => setFilters({ ...filters, start: event.target.value })} />
        <input type="date" value={filters.end} onChange={(event) => setFilters({ ...filters, end: event.target.value })} />
      </div>
      <form onSubmit={createReservation} className="reservation-form">
        <select required value={form.room} onChange={(event) => setForm({ ...form, room: event.target.value })}>
          <option value="">Choisir une salle</option>
          {rooms.map((room) => (
            <option key={room.id} value={room.id}>
              {room.name}
            </option>
          ))}
        </select>
        <input required placeholder="Objet de réunion" value={form.title} onChange={(event) => setForm({ ...form, title: event.target.value })} />
        <input placeholder="Description" value={form.description} onChange={(event) => setForm({ ...form, description: event.target.value })} />
        <input required type="datetime-local" value={form.start_datetime} onChange={(event) => setForm({ ...form, start_datetime: event.target.value })} />
        <input required type="datetime-local" value={form.end_datetime} onChange={(event) => setForm({ ...form, end_datetime: event.target.value })} />
        <select
          multiple
          value={form.participants}
          onChange={(event) =>
            setForm({
              ...form,
              participants: Array.from(event.target.selectedOptions, (option) => option.value),
            })
          }
        >
          {users.map((user) => (
            <option key={user.id} value={user.id}>
              {user.username}
            </option>
          ))}
        </select>
        <label>
          <input type="checkbox" checked={form.is_recurring} onChange={(event) => setForm({ ...form, is_recurring: event.target.checked })} />
          Réservation récurrente
        </label>
        {form.is_recurring && (
          <>
            <select value={form.frequency} onChange={(event) => setForm({ ...form, frequency: event.target.value })}>
              <option value="daily">Quotidienne</option>
              <option value="weekly">Hebdomadaire</option>
              <option value="monthly">Mensuelle</option>
            </select>
            <input type="number" min="1" value={form.interval} onChange={(event) => setForm({ ...form, interval: event.target.value })} />
            <input type="number" min="1" placeholder="Nombre d'occurrences" value={form.count} onChange={(event) => setForm({ ...form, count: event.target.value })} />
          </>
        )}
        <button type="submit">Créer la réservation</button>
      </form>
      <ReservationCalendar reservations={reservations} />
    </section>
  );
}
