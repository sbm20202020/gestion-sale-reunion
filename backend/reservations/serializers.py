from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from .models import RecurrenceRule, Reservation

User = get_user_model()


class RecurrenceRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurrenceRule
        fields = ["id", "frequency", "interval", "end_date", "count", "days_of_week"]


class ReservationSerializer(serializers.ModelSerializer):
    organizer = serializers.StringRelatedField(read_only=True)
    organizer_id = serializers.PrimaryKeyRelatedField(source="organizer", queryset=User.objects.all(), write_only=True, required=False)
    participants = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, required=False)
    recurrence_rule = RecurrenceRuleSerializer(required=False, allow_null=True)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "room",
            "organizer",
            "organizer_id",
            "title",
            "description",
            "start_datetime",
            "end_datetime",
            "participants",
            "is_recurring",
            "recurrence_rule",
            "recurrence_group",
        ]
        read_only_fields = ["id", "organizer", "recurrence_group"]

    def validate(self, attrs):
        start = attrs.get("start_datetime", getattr(self.instance, "start_datetime", None))
        end = attrs.get("end_datetime", getattr(self.instance, "end_datetime", None))
        room = attrs.get("room", getattr(self.instance, "room", None))

        if start and end and start >= end:
            raise serializers.ValidationError("La date de fin doit être après la date de début.")

        if room and start and end:
            conflicts = Reservation.objects.filter(room=room, start_datetime__lt=end, end_datetime__gt=start)
            if self.instance:
                conflicts = conflicts.exclude(pk=self.instance.pk)
            if conflicts.exists():
                raise serializers.ValidationError("Conflit détecté: la salle est déjà réservée pour ce créneau.")

        return attrs

    def _validate_occurrence_conflicts(self, room, occurrences):
        for start, end in occurrences:
            if Reservation.objects.filter(room=room, start_datetime__lt=end, end_datetime__gt=start).exists():
                raise serializers.ValidationError(
                    "Conflit détecté sur une occurrence de la série de réservations."
                )

    @transaction.atomic
    def create(self, validated_data):
        recurrence_data = validated_data.pop("recurrence_rule", None)
        participants = validated_data.pop("participants", [])
        request = self.context.get("request")

        if not validated_data.get("organizer") and request and request.user.is_authenticated:
            validated_data["organizer"] = request.user

        is_recurring = validated_data.get("is_recurring", False)
        if is_recurring and recurrence_data:
            rule = RecurrenceRule.objects.create(**recurrence_data)
            validated_data["recurrence_rule"] = rule

            occurrences = rule.build_occurrences(
                validated_data["start_datetime"], validated_data["end_datetime"], max_occurrences=365
            )
            self._validate_occurrence_conflicts(validated_data["room"], occurrences)

            first = None
            group = None
            for start, end in occurrences:
                reservation = Reservation.objects.create(
                    **{
                        **validated_data,
                        "start_datetime": start,
                        "end_datetime": end,
                    }
                )
                reservation.participants.set(participants)
                if first is None:
                    first = reservation
                    group = reservation.recurrence_group
                else:
                    reservation.recurrence_group = group
                    reservation.save(update_fields=["recurrence_group"])
            return first

        reservation = Reservation.objects.create(**validated_data)
        reservation.participants.set(participants)
        return reservation

    @transaction.atomic
    def update(self, instance, validated_data):
        recurrence_data = validated_data.pop("recurrence_rule", None)
        participants = validated_data.pop("participants", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if recurrence_data is not None:
            if instance.recurrence_rule:
                for attr, value in recurrence_data.items():
                    setattr(instance.recurrence_rule, attr, value)
                instance.recurrence_rule.save()
            elif recurrence_data:
                instance.recurrence_rule = RecurrenceRule.objects.create(**recurrence_data)

        instance.save()

        if participants is not None:
            instance.participants.set(participants)

        return instance
