from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient

from reservations.models import Reservation
from rooms.models import Room


@override_settings(USE_SQLITE_FOR_TESTS=True)
class ReservationConflictTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        user_model = get_user_model()
        self.user = user_model.objects.create_user(username="user1", password="password123")
        self.client.force_authenticate(user=self.user)
        self.room = Room.objects.create(name="Salle A", capacity=10, location="1er étage")

    def test_cannot_create_conflicting_reservation(self):
        start = timezone.now() + timedelta(days=1)
        end = start + timedelta(hours=1)
        Reservation.objects.create(
            room=self.room,
            organizer=self.user,
            title="Réunion existante",
            start_datetime=start,
            end_datetime=end,
        )

        payload = {
            "room": self.room.id,
            "title": "Nouveau créneau",
            "start_datetime": start.isoformat(),
            "end_datetime": end.isoformat(),
            "is_recurring": False,
        }
        response = self.client.post("/api/reservations/reservations/", payload, format="json")
        self.assertEqual(response.status_code, 400)

    def test_recurring_creation_fails_when_one_occurrence_conflicts(self):
        start = timezone.now() + timedelta(days=1)
        end = start + timedelta(hours=1)
        Reservation.objects.create(
            room=self.room,
            organizer=self.user,
            title="Conflit",
            start_datetime=start + timedelta(days=1),
            end_datetime=end + timedelta(days=1),
        )

        payload = {
            "room": self.room.id,
            "title": "Série",
            "start_datetime": start.isoformat(),
            "end_datetime": end.isoformat(),
            "is_recurring": True,
            "recurrence_rule": {
                "frequency": "daily",
                "interval": 1,
                "count": 3,
            },
        }
        response = self.client.post("/api/reservations/reservations/", payload, format="json")
        self.assertEqual(response.status_code, 400)
