from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    readonly_fields = ('uuid', 'date_joined', 'last_login')
    fieldsets = [
        (None, {"fields": ("username", "password", "uuid")}),
        ("개인정보", {"fields": ("first_name", "last_name", "email", "date_joined", "last_login", "short_description")}),
        (
            "권한",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
    ]
