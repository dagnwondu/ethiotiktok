from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        'username',
        'email',
        'user_type',
        'is_staff',
        'is_active',
    )

    list_filter = (
        'user_type',
        'is_staff',
        'is_active',
    )

    search_fields = ('username', 'email')

    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Information", {
            "fields": ("user_type", "middle_name"),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Information", {
            "fields": ("user_type", "middle_name"),
        }),
    )
