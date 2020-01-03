from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm

class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'username', 'first_name', 'last_name',]

admin.site.register(User, UserAdmin)
