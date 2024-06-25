from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as DefaultGroupAdmin, Group, User, UserAdmin as DefaultUserAdmin
from unfold.admin import ModelAdmin
from unfold.forms import UserCreationForm, UserChangeForm, AdminPasswordChangeForm

admin.site.unregister(User)
admin.site.unregister(Group)


def get_default_fieldsets(add: bool = False) -> tuple:
    return (
        (
            "Main",
            {
                "classes": ("tab",),
                "fields": (
                    ("username", "password1", "password2")
                    if add
                    else ("username", "password")
                ),
            },
        ),
        (
            "Personal info",
            {
                "fields": ("first_name", "last_name", "email"),
                "classes": ["tab"],
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ["tab"],
            },
        ),
    )


@admin.register(User)
class UserAdmin(ModelAdmin, DefaultUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    change_password_form = AdminPasswordChangeForm
    add_fieldsets = get_default_fieldsets(True)
    fieldsets = get_default_fieldsets()


@admin.register(Group)
class GroupAdmin(ModelAdmin, DefaultGroupAdmin):
    pass
