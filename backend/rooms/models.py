from django.db import models


class Equipment(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=120, unique=True)
    capacity = models.PositiveIntegerField()
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    equipments = models.ManyToManyField(Equipment, blank=True, related_name="rooms")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
