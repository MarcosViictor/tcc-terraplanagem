from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Extra", {"fields": ("nome", "papel", "ativo", "criado_em", "atualizado_em")}),
    )
    list_display = ("username", "email", "nome", "papel", "is_staff", "is_active")
    list_filter = ("papel", "is_staff", "is_active")
