from django import forms
from allauth.account.forms import SignupForm

from .models import ReferralInvite, UserProfile


class CustomSignupForm(SignupForm):
    invite_code = forms.CharField(
        required=False,
        label='Referral code'
    )

    def signup(self, request, user):
        return user


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = (
            'avatar',
            'bio',
        )


class ReferralInviteForm(forms.ModelForm):

    class Meta:
        model = ReferralInvite
        fields = (
            'email',
            'role',
        )
