from django.db import models
from core.models import BaseModel


class TelegramUser(BaseModel):
    full_name = models.CharField(max_length=200, null=True, blank=True)
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self): return self.full_name or self.telegram_id

    class Meta:
        db_table = "telegram_users"


class Food(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self): return self.name

    class Meta:
        db_table = "foods"


class UserFood(BaseModel):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name="foods")
    name = models.CharField(max_length=100)

    def __str__(self): return self.name

    class Meta:
        db_table = "user_foods"
        unique_together = ("user", "name")
