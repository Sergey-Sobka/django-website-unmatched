from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string


class User(AbstractUser):

    class Roles(models.TextChoices):
        USER = 'user', 'User'
        EDITOR = 'editor', 'Editor'
        ADMIN = 'admin', 'Admin'

    email = models.EmailField(
        unique=True
    )

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.USER
    )

    invited_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invited_users'
    )

    def __str__(self):
        return self.username


class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True
    )

    bio = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.user.username


class ReferralInvite(models.Model):

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        USED = 'used', 'Used'
        CANCELLED = 'cancelled', 'Cancelled'

    class InviteRoles(models.TextChoices):
        USER = 'user', 'User'
        EDITOR = 'editor', 'Editor'

    code = models.CharField(
        max_length=32,
        unique=True,
        blank=True
    )

    email = models.EmailField()

    role = models.CharField(
        max_length=20,
        choices=InviteRoles.choices,
        default=InviteRoles.USER
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_invites'
    )

    accepted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accepted_invites'
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    used_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = get_random_string(12).upper()

        super().save(*args, **kwargs)

    def use(self, user):
        self.accepted_by = user
        self.status = self.Status.USED
        self.used_at = timezone.now()
        self.save()

    def __str__(self):
        return f'{self.email} - {self.role}'
