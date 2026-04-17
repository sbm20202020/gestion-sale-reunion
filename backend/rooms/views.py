from rest_framework import permissions, viewsets

from .models import Equipment, Room
from .serializers import EquipmentSerializer, RoomSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_admin_role)


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [IsAdminOrReadOnly]


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.prefetch_related("equipments").all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        equipment_ids = self.request.query_params.getlist("equipment")
        if equipment_ids:
            queryset = queryset.filter(equipments__id__in=equipment_ids).distinct()
        return queryset
