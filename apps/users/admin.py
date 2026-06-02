from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ReferralInvite, User, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    extra = 0


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'is_staff',
        'is_superuser',
    )

    list_filter = (
        'role',
        'is_staff',
        'is_superuser',
        'is_active',
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            'Wiki info',
            {
                'fields': (
                    'role',
                    'invited_by',
                )
            }
        ),
    )

    inlines = (
        UserProfileInline,
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'bio',
    )

    search_fields = (
        'user__username',
        'bio',
    )


@admin.register(ReferralInvite)
class ReferralInviteAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'role',
        'code',
        'status',
        'created_by',
        'accepted_by',
    )

    list_filter = (
        'role',
        'status',
    )

    search_fields = (
        'email',
        'code',
    )
