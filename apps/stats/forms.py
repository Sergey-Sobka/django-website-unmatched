from django import forms

from .models import MatchRecord


class MatchRecordForm(forms.ModelForm):

    class Meta:
        model = MatchRecord
        fields = (
            'mode',
            'map',
            'team_one_player',
            'team_one_character',
            'team_one_partner',
            'team_two_player',
            'team_two_character',
            'team_two_partner',
            'winner',
            'played_at',
            'notes',
        )
        widgets = {
            'played_at': forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),
        }
