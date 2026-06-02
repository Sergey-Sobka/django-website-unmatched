from django import forms

from .models import Card, Character, GameSet, Map


class BootstrapModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


class GameSetForm(BootstrapModelForm):

    class Meta:
        model = GameSet
        fields = (
            'name',
            'release_year',
            'description',
            'bgg_link',
            'cover_image',
        )


class CharacterForm(BootstrapModelForm):

    class Meta:
        model = Character
        fields = (
            'game_set',
            'name',
            'subtitle',
            'description',
            'movement',
            'special',
            'quote',
            'health',
            'attack_type',
            'image',
        )


class MapForm(BootstrapModelForm):

    class Meta:
        model = Map
        fields = (
            'game_set',
            'name',
            'description',
            'players_count',
            'spaces_count',
            'zone_count',
            'image',
        )


class CardForm(BootstrapModelForm):

    class Meta:
        model = Card
        fields = (
            'character',
            'name',
            'card_type',
            'quantity',
            'value',
            'boost',
            'text',
            'image',
        )
