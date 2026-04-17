from rest_framework.routers import DefaultRouter

from .views import EquipmentViewSet, RoomViewSet

router = DefaultRouter()
router.register("equipments", EquipmentViewSet, basename="equipment")
router.register("rooms", RoomViewSet, basename="room")

urlpatterns = router.urls
