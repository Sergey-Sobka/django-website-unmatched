from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

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


class ReferralInviteListView(LoginRequiredMixin, ListView):
    template_name = 'users/referral_invite_list.html'
    context_object_name = 'invites'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('wiki:game-set-list')

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return ReferralInvite.objects.filter(
            created_by=self.request.user
        ).order_by('-created_at')


class ReferralInviteCreateView(LoginRequiredMixin, CreateView):
    model = ReferralInvite
    form_class = ReferralInviteForm
    template_name = 'users/referral_invite_form.html'
    success_url = reverse_lazy('users:referral-invite-list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('wiki:game-set-list')

        return super().dispatch(request, *args, **kwargs)

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


def referral_accept_view(request, code):
    request.session['invite_code'] = code

    return redirect(
        f'{reverse_lazy("account_signup")}?invite={code}'
    )
