from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Food, TelegramUser


@admin.register(Food)
class FoodAdmin(ModelAdmin):
    list_display = ("id", "name",)
    fields = ("name",)
    search_fields = list_display


@admin.register(TelegramUser)
class TelegramUserAdmin(ModelAdmin):
    list_display = ("id", "telegram_id", "full_name", "username",)
    fields = list_display
    search_fields = list_display
