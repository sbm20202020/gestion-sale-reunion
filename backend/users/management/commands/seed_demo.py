from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from reservations.models import Reservation
from rooms.models import Equipment, Room


class Command(BaseCommand):
    help = "Charge des données de démonstration"

    def handle(self, *args, **options):
        user_model = get_user_model()

        admin, _ = user_model.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@example.com", "role": "admin", "is_staff": True, "is_superuser": True},
        )
        admin.set_password("admin12345")
        admin.save()

        user, _ = user_model.objects.get_or_create(username="demo", defaults={"email": "demo@example.com", "role": "user"})
        user.set_password("demo12345")
        user.save()

        projector, _ = Equipment.objects.get_or_create(name="Projecteur", defaults={"quantity": 3})
        board, _ = Equipment.objects.get_or_create(name="Tableau blanc", defaults={"quantity": 5})

        room, _ = Room.objects.get_or_create(name="Salle Alpha", defaults={"capacity": 12, "location": "Bâtiment A"})
        room.equipments.set([projector, board])

        start = timezone.now() + timedelta(days=1)
        Reservation.objects.get_or_create(
            room=room,
            organizer=user,
            title="Démo réunion",
            start_datetime=start,
            end_datetime=start + timedelta(hours=1),
        )

        self.stdout.write(self.style.SUCCESS("Données de démonstration chargées."))
