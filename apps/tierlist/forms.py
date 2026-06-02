from django import forms

from .models import TierListEntry


class TierListEntryForm(forms.ModelForm):

    class Meta:
        model = TierListEntry
        fields = (
            'mode',
            'character',
            'tier',
            'notes',
        )
