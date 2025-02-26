from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from userAuth.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ('username',)
