from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from . import models

admin.site.site_header = "Consultation Network Admin"
admin.site.index_title = "Admin"

@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email',
                        'first_name', 'last_name'),
        }),
    )