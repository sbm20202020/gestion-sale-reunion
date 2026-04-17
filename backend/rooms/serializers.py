from rest_framework import serializers

from .models import Equipment, Room


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ["id", "name", "description", "quantity"]


class RoomSerializer(serializers.ModelSerializer):
    equipments = serializers.PrimaryKeyRelatedField(queryset=Equipment.objects.all(), many=True, required=False)

    class Meta:
        model = Room
        fields = ["id", "name", "capacity", "location", "description", "is_active", "equipments"]
