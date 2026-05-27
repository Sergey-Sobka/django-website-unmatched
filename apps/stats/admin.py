from django.contrib import admin

from .models import MatchRecord


@admin.register(MatchRecord)
class MatchRecordAdmin(admin.ModelAdmin):
    list_display = (
        'mode',
        'team_one_character',
        'team_two_character',
        'winner',
        'played_at',
        'created_by',
    )

    list_filter = (
        'mode',
        'winner',
        'played_at',
    )

    search_fields = (
        'team_one_player',
        'team_two_player',
        'team_one_character__name',
        'team_two_character__name',
    )
