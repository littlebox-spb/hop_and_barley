from typing import TYPE_CHECKING

from django.contrib import admin

from .models import User

if TYPE_CHECKING:
    ModelAdminUser = admin.ModelAdmin[User]
else:
    ModelAdminUser = admin.ModelAdmin


@admin.register(User)
class UserAdmin(ModelAdminUser):
    list_display = ("username", "email", "phone", "is_staff")
    search_fields = ("username", "email", "phone")
