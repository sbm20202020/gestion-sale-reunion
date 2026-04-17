from django.contrib import admin

from .models import RecurrenceRule, Reservation


@admin.register(RecurrenceRule)
class RecurrenceRuleAdmin(admin.ModelAdmin):
    list_display = ("frequency", "interval", "end_date", "count")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("title", "room", "organizer", "start_datetime", "end_datetime", "is_recurring")
    list_filter = ("room", "is_recurring")
    filter_horizontal = ("participants",)
