from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    RedirectView,
    TemplateView,
    UpdateView,
)

from .forms import ReferralInviteForm, UserProfileForm
from .models import ReferralInvite


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user.profile


class ReferralInviteListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'users/referral_invite_list.html'
    context_object_name = 'invites'
    permission_required = 'users.view_referralinvite'

    def get_queryset(self):
        return ReferralInvite.objects.filter(
            created_by=self.request.user
        ).order_by('-created_at')


class ReferralInviteCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ReferralInvite
    form_class = ReferralInviteForm
    template_name = 'users/referral_invite_form.html'
    success_url = reverse_lazy('users:referral-invite-list')
    permission_required = 'users.add_referralinvite'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        invite_link = self.request.build_absolute_uri(
            reverse_lazy('users:referral-accept', kwargs={'code': self.object.code})
        )

        send_mail(
            'Unmatched Wiki invite',
            f'Use this invite link to register: {invite_link}',
            None,
            [self.object.email],
        )

        messages.success(
            self.request,
            f'Invite was created. Code: {self.object.code}'
        )

        return response


class ReferralAcceptView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        code = kwargs['code']
        self.request.session['invite_code'] = code

        return f'{reverse_lazy("account_signup")}?invite={code}'
