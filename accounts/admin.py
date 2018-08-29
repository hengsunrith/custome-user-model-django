# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.contrib.auth import get_user_model
from accounts.models import GuestEmail, Profile
from accounts.forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin', 'staff', 'active', 'timestamp')
    list_filter = ('admin', 'staff', 'active')
    fieldsets = (
        (None, {'fields': ('full_name', 'email', 'password')}),
        # ('Personal info', {'fields': ('full_name', )}),
        ('Permissions', {'fields': ('admin', 'staff', 'active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', 'full_name')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)


class GuessEmailAdmin(admin.ModelAdmin):
    search_fields = ['email']
    list_display = ('email', 'active', 'update')

    class Meta:
        model = GuestEmail


admin.site.register(GuestEmail, GuessEmailAdmin)


admin.site.register(Profile)