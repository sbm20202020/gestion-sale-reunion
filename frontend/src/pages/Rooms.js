import { useEffect, useMemo, useState } from 'react';

import api from '../services/api';

export default function RoomsPage() {
  const [rooms, setRooms] = useState([]);
  const [equipments, setEquipments] = useState([]);
  const [filterEquipment, setFilterEquipment] = useState('');

  useEffect(() => {
    api.get('/rooms/equipments/').then((response) => setEquipments(response.data));
    api.get('/rooms/rooms/').then((response) => setRooms(response.data));
  }, []);

  useEffect(() => {
    const query = filterEquipment ? { params: { equipment: filterEquipment } } : undefined;
    api.get('/rooms/rooms/', query).then((response) => setRooms(response.data));
  }, [filterEquipment]);

  const equipmentMap = useMemo(
    () => Object.fromEntries(equipments.map((equipment) => [equipment.id, equipment.name])),
    [equipments]
  );

  return (
    <section className="card">
      <h1>Salles</h1>
      <select value={filterEquipment} onChange={(event) => setFilterEquipment(event.target.value)}>
        <option value="">Tous les équipements</option>
        {equipments.map((equipment) => (
          <option value={equipment.id} key={equipment.id}>
            {equipment.name}
          </option>
        ))}
      </select>
      <div className="grid">
        {rooms.map((room) => (
          <article key={room.id} className="room-card">
            <h3>{room.name}</h3>
            <p>Capacité : {room.capacity}</p>
            <p>Localisation : {room.location}</p>
            <p>Équipements : {room.equipments.map((id) => equipmentMap[id]).filter(Boolean).join(', ') || 'Aucun'}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
