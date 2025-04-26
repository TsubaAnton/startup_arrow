from django.db import models
from users.models import User

NULLABLE = {"blank": True, "null": True}


class Route(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="routes")
    start_lat = models.FloatField()
    start_lng = models.FloatField()
    end_lat = models.FloatField()
    end_lng = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
