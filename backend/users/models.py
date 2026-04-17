from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Administrateur"
        USER = "user", "Utilisateur"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    phone = models.CharField(max_length=32, blank=True)
    department = models.CharField(max_length=150, blank=True)

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN or self.is_staff
