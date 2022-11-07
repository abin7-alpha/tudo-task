from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Account

class AccountAdmin(UserAdmin):
    list_display = ('email','date_joined', 'last_login', 'is_admin','is_staff','is_superuser','is_active')
    search_fields = ('email',)
    readonly_fields=('date_joined', 'last_login',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active')}
        ),
    )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
