import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';

export default function ReservationCalendar({ reservations }) {
  const events = reservations.map((reservation) => ({
    id: reservation.id,
    title: reservation.title,
    start: reservation.start_datetime,
    end: reservation.end_datetime,
    backgroundColor: `hsl(${(reservation.room * 40) % 360}, 70%, 45%)`,
  }));

  return (
    <FullCalendar
      plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
      initialView="timeGridWeek"
      headerToolbar={{
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay',
      }}
      events={events}
      height="auto"
    />
  );
}
