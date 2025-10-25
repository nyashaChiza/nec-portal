from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

# Register your models here.
User = get_user_model()

class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = (User.USERNAME_FIELD, 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': (User.USERNAME_FIELD, 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email','role')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (User.USERNAME_FIELD, 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    search_fields = (User.USERNAME_FIELD, 'email')
    ordering = (User.USERNAME_FIELD,)

admin.site.register(User, UserAdmin)