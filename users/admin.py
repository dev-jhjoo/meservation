from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from users.models import User
from django.utils.translation import gettext_lazy as _

class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('nickname', 'email')

class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('nickname', 'uuid', 'password', 'email')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'description')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('create_at', 'update_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nickname', 'email', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('create_at','update_at','uuid')

    form = UserChangeForm
    add_form = UserCreateForm
    list_display = ('nickname', 'email', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('nickname', 'email')
    ordering = ('nickname',)

admin.site.register(User, UserAdmin)
    