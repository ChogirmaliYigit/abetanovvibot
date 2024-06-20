from django.db import models


class TelegramUser(models.Model):
    full_name = models.CharField(max_length=200, null=True, blank=True)
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self): return self.full_name or self.telegram_id

    class Meta:
        db_table = "telegram_users"


class Food(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self): return self.name

    class Meta:
        db_table = "foods"
