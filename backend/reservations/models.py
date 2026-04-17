import uuid
from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from rooms.models import Room


class RecurrenceRule(models.Model):
    class Frequency(models.TextChoices):
        DAILY = "daily", "Quotidienne"
        WEEKLY = "weekly", "Hebdomadaire"
        MONTHLY = "monthly", "Mensuelle"

    frequency = models.CharField(max_length=20, choices=Frequency.choices)
    interval = models.PositiveIntegerField(default=1)
    end_date = models.DateField(null=True, blank=True)
    count = models.PositiveIntegerField(null=True, blank=True)
    days_of_week = models.CharField(max_length=32, blank=True, help_text="0=lundi ... 6=dimanche")

    def __str__(self):
        return f"{self.frequency} / {self.interval}"

    def build_occurrences(self, start_datetime, end_datetime, max_occurrences=365):
        occurrences = []
        current_start = start_datetime
        current_end = end_datetime

        weekdays = set()
        if self.days_of_week:
            weekdays = {int(day.strip()) for day in self.days_of_week.split(",") if day.strip().isdigit()}

        while len(occurrences) < max_occurrences:
            if self.end_date and current_start.date() > self.end_date:
                break
            if self.count and len(occurrences) >= self.count:
                break

            if self.frequency != self.Frequency.WEEKLY or not weekdays or current_start.weekday() in weekdays:
                occurrences.append((current_start, current_end))

            if self.frequency == self.Frequency.DAILY:
                delta = timedelta(days=self.interval)
                current_start += delta
                current_end += delta
            elif self.frequency == self.Frequency.WEEKLY:
                delta = timedelta(days=1)
                current_start += delta
                current_end += delta
            else:
                next_month = current_start.month + self.interval
                year = current_start.year + ((next_month - 1) // 12)
                month = ((next_month - 1) % 12) + 1
                day = min(current_start.day, 28)
                current_start = current_start.replace(year=year, month=month, day=day)
                current_end = current_start + (end_datetime - start_datetime)

        return occurrences


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reservations")
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="organized_reservations")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="participating_reservations", blank=True)
    is_recurring = models.BooleanField(default=False)
    recurrence_rule = models.ForeignKey(RecurrenceRule, on_delete=models.SET_NULL, null=True, blank=True, related_name="reservations")
    recurrence_group = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)

    class Meta:
        ordering = ["start_datetime"]

    def clean(self):
        if self.start_datetime >= self.end_datetime:
            raise ValidationError("La date de fin doit être après la date de début.")

    def __str__(self):
        return f"{self.title} ({self.room})"
