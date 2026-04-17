from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import AdminUserViewSet, ParticipantListView, ProfileView, RegisterView

router = DefaultRouter()
router.register("users", AdminUserViewSet, basename="admin-users")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("participants/", ParticipantListView.as_view(), name="participants"),
]

urlpatterns += router.urls
