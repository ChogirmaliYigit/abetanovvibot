# Generated by Django 5.0.6 on 2024-06-25 18:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tgbot", "0004_alter_userfood_unique_together"),
    ]

    operations = [
        migrations.AddField(
            model_name="telegramuser",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]