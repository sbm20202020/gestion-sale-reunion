from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .models import Reservation
from .serializers import ReservationSerializer


class IsAdminOrOrganizer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user.is_authenticated and (request.user.is_admin_role or obj.organizer_id == request.user.id))


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.select_related("room", "organizer", "recurrence_rule").prefetch_related("participants")
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOrganizer]

    def get_queryset(self):
        queryset = super().get_queryset()
        room_id = self.request.query_params.get("room")
        user_id = self.request.query_params.get("user")
        start_date = self.request.query_params.get("start")
        end_date = self.request.query_params.get("end")

        if room_id:
            queryset = queryset.filter(room_id=room_id)
        if user_id:
            queryset = queryset.filter(organizer_id=user_id)
        if start_date:
            queryset = queryset.filter(end_datetime__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(start_datetime__date__lte=end_date)

        return queryset

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    def update(self, request, *args, **kwargs):
        scope = request.query_params.get("scope", "single")
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        if scope != "series" or not instance.is_recurring:
            return super().update(request, partial=partial, *args, **kwargs)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        participants = data.pop("participants", None)

        reservations = Reservation.objects.filter(recurrence_group=instance.recurrence_group)
        for reservation in reservations:
            for attr, value in data.items():
                setattr(reservation, attr, value)
            reservation.save()
            if participants is not None:
                reservation.participants.set(participants)

        return Response(self.get_serializer(instance).data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        scope = request.query_params.get("scope", "single")
        instance = self.get_object()

        if scope == "series" and instance.is_recurring:
            Reservation.objects.filter(recurrence_group=instance.recurrence_group).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return super().destroy(request, *args, **kwargs)
