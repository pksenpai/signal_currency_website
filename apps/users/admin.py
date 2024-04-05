from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib import admin

from .models import CustomUser, Profile
from .forms import UserRegisterForm, UserUpdateForm


class CustomUserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserUpdateForm
    add_form = UserRegisterForm

    list_display = ["username", "phone_number"]
    list_filter = ["is_admin"]
    fieldsets = [
        ("Base Data", {"fields": ["is_active", "username", "password", "country", "phone_number"]}),
        ("Permissions", {"fields": ["is_admin"]}),
        ("Info", {"fields": ["email"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["username", "password1", "password2", "phone_number", "country"],
            },
        ),
    ]
    search_fields = ["username"]
    ordering = ["username"]
    filter_horizontal = []


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)

# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
