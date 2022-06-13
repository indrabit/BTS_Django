from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username']
    readonly_fields = ['last_login', 'date_joined']
    exclude = ['password', 'is_superuser']
    search_fields = ['email']


# Register your models here.
admin.site.register(User, UserAdmin)