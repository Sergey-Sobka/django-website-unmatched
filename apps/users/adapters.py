from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth.models import Group, Permission

from .models import ReferralInvite, User


class AccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)

        invite_code = self.get_invite_code(request, form)
        invite = self.get_invite(invite_code, user.email)

        if invite:
            user.role = invite.role
            user.invited_by = invite.created_by

            if invite.role == User.Roles.EDITOR:
                user.is_staff = True

        if commit:
            user.save()

            if invite:
                invite.use(user)
                self.add_editor_permissions(user)

        return user

    def get_invite_code(self, request, form):
        if form and hasattr(form, 'cleaned_data'):
            invite_code = form.cleaned_data.get('invite_code')

            if invite_code:
                return invite_code

        return request.GET.get('invite') or request.session.get('invite_code')

    def get_invite(self, invite_code, email):
        if not invite_code:
            return None

        return ReferralInvite.objects.filter(
            code=invite_code,
            email__iexact=email,
            status=ReferralInvite.Status.ACTIVE,
        ).first()

    def add_editor_permissions(self, user):
        if user.role != User.Roles.EDITOR:
            return

        group, _ = Group.objects.get_or_create(
            name='Editors'
        )

        permissions = Permission.objects.filter(
            content_type__app_label__in=[
                'wiki',
                'stats',
                'tierlist',
            ]
        )
        group.permissions.set(permissions)
        user.groups.add(group)
